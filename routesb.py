
###############################################################################################
from flask import Flask, render_template, url_for, redirect
from flask_oidc import OpenIDConnect
from okta import UsersClient
from werkzeug import secure_filename
from flask import Flask, request, redirect, url_for, render_template
from knackpy import Knack
import knackpy
import pandas as pd
from os import environ



app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'this is my secret key today',
    'OIDC_CLIENT_SECRETS': './client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_SCOPES': ["openid", "profile", "email"],
    'OIDC_CALLBACK_ROUTE': '/authorization-code/callback'
})



oidc = OpenIDConnect(app)

okta_client = UsersClient("https://dev-853077.oktapreview.com", "00kkeceedfUe6CsfZgBILYHMSEqiyS82n19C7mrKWk")

@app.route("/")
def index():
  return render_template("index.html", oidc=oidc)


@app.route("/about")
def about():
  return render_template("about.html",oidc=oidc)


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for("profile"))


# @app.route("/profile")
# def profile():
#     info = oidc.user_getinfo(["sub", "name", "email"])
#     return render_template("profile.html", profile=info, oidc=oidc)
# @app.route('/profile', methods=['GET', 'POST'])
# def profile():
#     info = oidc.user_getinfo(["sub", "name", "email"])
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             print('No file attached in request')
#             return redirect(request.url)
#         df_knack =  pd.read_csv(request.files.get('file'))
#         df_knack.columns = cols.values()
#
#         #fill all empty values with 'N/A'
#         df_knack.fillna(value="N/A", axis=1, inplace=True)
#
#        # Ectract other non objects values in their dataframe
#         df_knack_sub1 = df_knack.iloc[::, 2:5]
#         df_knack_sub2 = df_knack.iloc[::, 10:38]
#         df_knack_sub = pd.concat([df_knack_sub1,df_knack_sub2], axis=1)
#         # convert data into dict
#         df_knack_sub_dict = df_knack_sub.to_dict(orient='records')
#         # only retrieve those with values
#         dict_with_values = []
#         for dict_data in df_knack_sub_dict :
#             dic = {i:j for i,j in dict_data.items() if j != 'N/A'}
#             dict_with_values.append(dic)
#         # lets get the name objects
#         bio_object = df_knack.iloc[::,0:2]
#         bio_object_dict = bio_object.to_dict(orient='records')
#
#        #lets get address objects
#         address_object = df_knack.iloc[::,5:10]
#         address_object.columns = address_object.columns.str.lower()
#         address_object_dict = address_object.to_dict(orient='records')
#
#         bio_val = []
#         for i, dicti in enumerate(dict_with_values):
#             dicti['field_298']= bio_object_dict[i]
#             bio_val.append(dicti)
#
#         bio_val_addr = []
#         for i, dicti in enumerate(bio_val ):
#             dicti["field_301"]= address_object_dict[i]
#             bio_val_addr.append(dicti)
#         all_data = []
#         for record in bio_val:
#             response = knackpy.record(
#             record,
#             obj_key='object_17',
#             app_id='59ca76c0e4c83424df3eee62',
#             api_key = 'a0998110-a889-11e7-9b23-7d5afe966012',
#             method='create')
#             all_data.append(record)
#         output = pd.DataFrame(all_data)
#         text = '{} records successfully loaded into Knack'.format(output.shape[0])
#         return render_template('profile.html', text=text, oidc=oidc)
#     return render_template("profile.html", profile=info, oidc=oidc)

cols = {
 "First":"first",
"Last":"last",
"Company is sponsor user":"field_300",
"SU":"field_432",
"Company name":"field_326",
"Address":"street",
"Zip":"zip",
"City":"city",
"State":"state",
"Country":"country",
"Time zone":"field_640",
"Recruiting source":"field_605",
"Phone":"field_302",
"Email":"field_303",
"LinkedIn profile":"field_304",
"Total compensation this year":"field_325",
"Personas":"field_306",
"Date added":"field_594",
"Last updated":"field_595",
"Updated by":"field_804",
"Wants to participate in future activities?":"field_596",
"Age range":"field_597",
"Years in current role":"field_601",
"Years in current industry":"field_602",
"Job duties":"field_603",
"Time Zone Selector":"field_606",
"Tome Zone Hours":"field_607",
"Current Time Equation":"field_608",
"Business Model":"field_794",
"Company size":"field_795",
"Company Revenue":"field_796",
"Team size":"field_797",
"Industry":"field_800",
"Job title":"field_801",
"Role/Responsibilities":"field_802",
"WCE Products used":"field_803",
"UserTesting ID":"field_805",
"id":"id"
}



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    kn = Knack(
          obj='object_17',
          app_id='59ca76c0e4c83424df3eee62',
          api_key='a0998110-a889-11e7-9b23-7d5afe966012 '
        )
    info = oidc.user_getinfo(["sub", "name", "email"])
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        knack_csv=  pd.read_csv(request.files.get('file'))
        knack_db = pd.DataFrame(kn.data)
        knack_db.drop('Email',  axis=1, inplace=True)
        knack_db['LinkedIn profile'] = knack_db['LinkedIn profile_url']
          #rename knack data to fit the new data
        knack_db.rename(columns={'Participant Name_first': 'First','Participant Name_last':'Last' ,
                 'Address_city':'City', 'Email_email':'Email', 'Address_street':'street', 'Address_country':'Country', 'Address_state':'State','Address_zip' : 'Zip'}, inplace=True)
        knack_db.id=''
        knack_db.drop(
           ['Address_latitude','Address_longitude', 'Address',
                     'Participant Name_middle','Participant Name_title',], axis=1, inplace=True)

        knack_db = knack_db[knack_csv.columns.tolist()]
        knack_db['Current Time Equation'] = ''
        knack_db['Date added']= ''
        knack_db['Last updated'] = ''
        knack_db.Phone  = knack_db.Phone.apply(pd.Series).iloc[::,3:4]

        for col in knack_csv.columns.tolist():
            knack_csv[col]= knack_csv[col].astype('object')

        for col in knack_csv.columns.tolist():
            knack_csv[col]= knack_csv[col].astype('object')

        list_of_columns = ['First', 'Last', 'Company is sponsor user', 'SU', 'Company name', 'street','Zip','City', 'State', 'Country',
                          'Time zone',
       'Recruiting source', 'Phone', 'Email', 'LinkedIn profile',
       'Total compensation this year', 'Personas', 'Date added',
       'Last updated', 'Updated by','Wants to participate in future activities?', 'Age range',
       'Years in current role', 'Years in current industry', 'Job duties',
       'Time Zone Selector', 'Tome Zone Hours', 'Current Time Equation','Business Model', 'Company size', 'Company Revenue', 'Team size',
       'Industry', 'Job title', 'Role/Responsibilities', 'WCE Products used',
       'UserTesting ID', 'id']

        knack_csv = knack_csv[list_of_columns]
        knack_csv = knack_csv.apply(lambda x: x.astype('str'))
        knack_csv = knack_csv.replace('nan','', regex=True)
        knack_csv['Company size'] = knack_csv['Company size'].str.split('.', expand=True)[0]

        knack_db = knack_db[list_of_columns]
        knack_db = knack_db.apply(lambda x: x.astype('str'))
        knack_db = knack_db.replace('nan','', regex=True)

        knack_csv = knack_csv.apply(lambda x: x.str.title())
        knack_db = knack_db.apply(lambda x: x.str.title())

        knack_csv = knack_csv.astype(knack_db.dtypes.to_dict())
        df_knack = knack_csv.merge(knack_db, how='left', indicator=True)
        received = df_knack.shape[0]
        df_knack = df_knack[df_knack['_merge']=='left_only']
        df_knack.drop('_merge', axis=1, inplace=True)


        df_knack.columns = cols.values()
        # Ectract other non objects values in their dataframe
        df_knack_sub1 = df_knack.iloc[::, 2:5]
        df_knack_sub2 = df_knack.iloc[::, 10:38]
        df_knack_sub = pd.concat([df_knack_sub1,df_knack_sub2], axis=1)

        # convert data into dict
        df_knack_sub_dict = df_knack_sub.to_dict(orient='records')


        # only retrieve those with values
        dict_with_values = []
        for dict_data in df_knack_sub_dict :
            dic = {i:j for i,j in dict_data.items() if j != 'N/A'}
            dict_with_values.append(dic)

        # lets get the name objects
        bio_object = df_knack.iloc[::,0:2]
        bio_object_dict = bio_object.to_dict(orient='records')

        #lets get address objects
        address_object = df_knack.iloc[::,5:10]
        address_object.columns = address_object.columns.str.lower()
        address_object_dict = address_object.to_dict(orient='records')

        bio_val = []
        for i, dicti in enumerate(dict_with_values):
            dicti['field_298']= bio_object_dict[i]
            bio_val.append(dicti)

        bio_val_addr = []
        for i, dicti in enumerate(bio_val ):
            dicti["field_301"]= address_object_dict[i]
            bio_val_addr.append(dicti)

        all_data = []
        for record in bio_val_addr:
            response = knackpy.record(
            record,
            obj_key='object_17',
            app_id='59ca76c0e4c83424df3eee62',
            api_key = 'a0998110-a889-11e7-9b23-7d5afe966012',
            method='create')
            all_data.append(record)
        # output = pd.DataFrame(all_data)
        text = '{} records received, {} unique record succesfully loaded into Knack'.format(received, len(all_data))
        return render_template('profile.html', text=text, oidc=oidc)
    return render_template("profile.html", profile=info, oidc=oidc)



@app.route("/logout", methods=["POST"])
def logout():
    oidc.logout()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host="localhost", port=8080,debug=True)

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         df = pd.read_csv(request.files.get('file'))
#         return render_template('upload.html', shape=df.shape)
#     return render_template('upload.html'
