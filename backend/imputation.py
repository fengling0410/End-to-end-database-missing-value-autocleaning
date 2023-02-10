import sqlite3
import sqlite3
from turtle import left
from matplotlib.pyplot import table
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors
from sklearn.metrics import mean_squared_error 
from math import sqrt
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
import numpy as np

subset_imputation_flag = True


def getTableSchema(conn, table_name):
    res = []
    for row in conn.execute(f"PRAGMA table_info('{table_name}')").fetchall():
        res.append(row[1])
    return res

def merge(conn, data, column_to_impute, foreign_keys):
    try: 
        key_ls = set()
        if foreign_keys != "":
            fks = foreign_keys.split(";")
            for fk in fks: 
                fk = fk.strip()
                print(f"Foreign key: {fk}")
                left_key, other = fk.split(":")
                left_key = left_key.strip()
                other = other.strip()
            
                table_to_merge, right_key = other.split(",")
                table_to_merge = table_to_merge.strip()
                right_key = right_key.strip()
            
                print(f"Left key: {left_key}")
                print(f"Right table: {table_to_merge}")
                print(f"Right key: {right_key}")
                key_ls.add(left_key)
                key_ls.add(right_key)
                print("--------------------------")
                print("Merging table %s" % (table_to_merge))

                # Check if the left column has some missing values 
                if sum(data[left_key].isnull()) > 0: 
                    if left_key == column_to_impute:
                        # Scenario 2a
                        print(f"Cannot merge: there are missing values on {left_key} and it is the column to impute")
                        continue
                    else: 
                        # Scenario 2b, drop the rows with NA
                        data.dropna(subset=[left_key])

            
                # Now, left column has no missing values 
                # Scenario 3
                data_to_merge = conn.execute("SELECT * FROM %s" % (table_to_merge)).fetchall()
                data_to_merge = pd.DataFrame(data_to_merge, columns = getTableSchema(conn, "%s" % (table_to_merge)))
                merged_df = data.merge(data_to_merge, how = "left", 
                                        left_on=left_key, 
                                        right_on=right_key,
                                        suffixes=("", "_y"))
                new_cols = list(merged_df.columns)
                print(f"New columns of merged table: {new_cols}")
                dup_col = right_key + "_y" # remove duplicated columns
                if dup_col in new_cols:
                    new_cols.remove(dup_col)                       
                data = merged_df[new_cols]
    except:
        return None, set()

            
    return data, key_ls

def process_data(conn, table_to_impute, column_to_impute, foreign_keys, input_query): 
    try:
        data = conn.execute("SELECT * FROM %s" % (table_to_impute)).fetchall()
        data = pd.DataFrame(data, columns = getTableSchema(conn, "%s" % (table_to_impute)))

        # Not consider input query if there is any aggregation 
        # Just impute the whole table for users
        agg_list = ["min", "max", "avg", "group by", "having", "count", "sum"]
        input_query = input_query.lower()
        impute_whole_data = False 
        for word in agg_list: 
            if input_query.find(word) != -1:
                impute_whole_data = True

        # Process foreign key-primary key relationship
        # Merge
        cond = None

        data, key_ls = merge(conn, data, column_to_impute, foreign_keys)

        if data is None: 
            return None, set(), None

        if impute_whole_data == True or subset_imputation_flag == False:
            return data, key_ls, cond

        # Get rows that user needed  
        if impute_whole_data == False:
            if input_query.find("where") != -1:
                # If there is no where clause, we can skip filtering
                temp = input_query.split("where")
                cond = temp[1]
                print(f"Conditions: {cond}")     

        return data, key_ls, cond

    except Exception as exp: 
        print(type(exp))
        print(exp)
        return None, set(), None


def impute_missing_values(sql_path, table_to_impute, column_to_impute, input_query, foreign_keys): 
    # Get all tables 
    def sql_fetch(conn):
        # Return all table names
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT name from sqlite_master where type= "table"')
        return cursorObj.fetchall() 

    conn = sqlite3.connect(sql_path)
    tables = sql_fetch(conn)
    print(f"Tables in current database: {tables}")

    df, key_ls, cond = process_data(conn, table_to_impute, column_to_impute, foreign_keys, input_query)
    
    if df is None: 
        return None, "invalid input"
    else: 
        return imputation(df, column_to_impute, key_ls, cond)
       

def imputation(whole_data, column_to_impute, key_ls, condition = None):
    print(f"Input columns: {list(whole_data.columns)}")
    col = whole_data[column_to_impute]
    n = len(whole_data)
    print("Unique value percentage: %.4f " % (len(col.unique()) / n))
    if col.dtype.kind not in 'iufc' and (n - len(col.unique())) / n < 0.5: 
        return None, "unique value error"  # cannot impute
    if col.dtype.kind not in 'iufc':
        whole_data[column_to_impute] = pd.Categorical(col)
    col = whole_data[column_to_impute]
    cols = []
    for i in whole_data.columns:
        if i == column_to_impute:
            cols.append(i)
        elif i in key_ls:
            continue
        elif whole_data[i].dtype.kind in 'iufc' or whole_data[i].dtype.name == 'category':
            cols.append(i)
        elif (n - len(whole_data[i].unique())) / n >= 0.5:
            whole_data[i] = pd.Categorical(whole_data[i])
            cols.append(i)
    dat = whole_data[cols]
    df = dat.dropna()
    if len(df) > 10000:
        df = df.sample(n=10000)
    new_df = pd.get_dummies(df.drop(column_to_impute,axis=1))
    new_df[column_to_impute] = df[column_to_impute]

    train , test = train_test_split(new_df, test_size = 0.3)
    x_train = train.drop(column_to_impute, axis=1)
    y_train = train[column_to_impute]
    x_test = test.drop(column_to_impute, axis=1)
    y_test = test[column_to_impute]
    scaler = MinMaxScaler(feature_range=(0, 1))
    x_train_scaled = scaler.fit_transform(x_train)
    x_train = pd.DataFrame(x_train_scaled)
    x_test_scaled = scaler.fit_transform(x_test)
    x_test = pd.DataFrame(x_test_scaled)
    string = ""
    model = None
    if col.dtype.name == 'category':
        string += "Accuracy_"
        model_knn, acc_knn = KNN_classification(x_train,y_train,x_test,y_test)
        model_rf, acc_rf = RandomForest_classification(x_train, y_train, x_test, y_test)
        if acc_knn > acc_rf:
            model = model_knn
            string += str(round(acc_knn,2))
        else:
            model = model_rf
            string += str(round(acc_rf,2)) 
    else:
        string += "RMSE_"
        model_knn, error_knn = KNN_regression(x_train,y_train,x_test,y_test)
        model_rf, error_rf = RandomForest_regression(x_train, y_train, x_test, y_test)
        if error_knn < error_rf:
            model = model_knn
            string += str(round(error_knn,2))
        else:
            model = model_rf
            string += str(round(error_rf,2))
    subset_index = range(len(whole_data))
    if condition:
        subset_index = subset(whole_data,condition)
    X = pd.get_dummies(dat.drop(column_to_impute,axis=1))
    X = scaler.fit_transform(X)
    if col.dtype.name == 'category':
        for i in subset_index:
            if dat.loc[i,column_to_impute]:
                whole_data.loc[i,column_to_impute] = model.predict(X[i,:].reshape(1,-1))
    else:
        for i in subset_index:
            if np.isnan(dat.loc[i,column_to_impute]):
                whole_data.loc[i,column_to_impute] = model.predict(X[i,:].reshape(1,-1))
    
    return whole_data.iloc[subset_index,:], string
    
def KNN_classification(x_train,y_train,x_test,y_test):      
    model = neighbors.KNeighborsClassifier(n_neighbors=int(sqrt(len(x_train))))
    model.fit(x_train,y_train)
    pred = model.predict(x_test)
    acc = sum(y_test==pred) / len(pred)
    return model, acc

def KNN_regression(x_train,y_train,x_test,y_test):
    model = neighbors.KNeighborsRegressor(n_neighbors=int(sqrt(len(x_train))))
    model.fit(x_train,y_train)
    pred = model.predict(x_test)
    error = sqrt(mean_squared_error(y_test,pred))
    return model, error

def RandomForest_classification(x_train,y_train,x_test,y_test):
    model = RandomForestClassifier()
    model.fit(x_train,y_train)
    pred = model.predict(x_test)
    acc = sum(y_test==pred) / len(pred)
    return model, acc

def RandomForest_regression(x_train,y_train,x_test,y_test):
    model = RandomForestRegressor()
    model.fit(x_train,y_train)
    pred = model.predict(x_test)
    error = sqrt(mean_squared_error(y_test,pred))
    return model, error

def subset(dat, condition):
    l = list(condition.split())
    i = 0
    while i < len(l):
        col = l[i].split(".")[1]
        op = l[i+1]
        val = l[i+2]
        if '\"' in val:
            # string fields
            val = val.replace('\"','')
            if op == "=":
                dat = dat[dat[col] == val]
            else:
                dat = dat[~(dat[col] == val)]
        else:
            # numeric fields
            val = float(val)
            if op == ">":
                dat = dat[dat[col] > val]
            elif op == ">=":
                dat = dat[dat[col] >= val]
            elif op == "<":
                dat = dat[dat[col] < val]
            elif op == "<=":
                dat = dat[dat[col] <= val]
            elif op == "=":
                dat = dat[dat[col] == val]
            else:
                dat = dat[~(dat[col] == val)]
        
        i += 4

    return dat.index
                
