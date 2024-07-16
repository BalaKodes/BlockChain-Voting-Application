from flask import Flask,render_template,request,redirect,session
from web3 import Web3,HTTPProvider
import json

def connect_with_register():
    web3=Web3(HTTPProvider('http://127.0.0.1:7545'))
    web3.eth.defaultAccount=web3.eth.accounts[0]

    with open('../build/contracts/register.json') as f:
        artifact_json=json.load(f)
        contract_abi=artifact_json['abi']
        contract_address=artifact_json['networks']['5777']['address']
    
    contract=web3.eth.contract(abi=contract_abi,address=contract_address)
    return contract,web3

def connect_with_voting():
    web3=Web3(HTTPProvider('http://127.0.0.1:7545'))
    web3.eth.defaultAccount=web3.eth.accounts[0]

    with open('../build/contracts/voting.json') as f:
        artifact_json=json.load(f)
        contract_abi=artifact_json['abi']
        contract_address=artifact_json['networks']['5777']['address']
    
    contract=web3.eth.contract(abi=contract_abi,address=contract_address)
    return contract,web3

app=Flask(__name__)
app.secret_key='1234'

@app.route('/')
def homePage():
    return render_template('navigation.html')

@app.route('/index')
def indexPage():
    return render_template('index.html')

@app.route('/voters')
def voters():
    contract,web3=connect_with_register()
    _names,_adhars,_mobiles,_dobs,_states,_districts,_pincodes,_=contract.functions.viewUsers().call()
    data=[]
    for i in range(len(_names)):
        dummy=[]
        dummy.append(_names[i])
        dummy.append(_adhars[i])
        dummy.append(_mobiles[i])
        dummy.append(_dobs[i])
        dummy.append(_states[i])
        dummy.append(_districts[i])
        dummy.append(_pincodes[i])
        data.append(dummy)
    return render_template('data.html',dashboard_data=data,l=len(data))

@app.route('/people')
def people():
    contract,web3=connect_with_register()
    _names,_adhars,_mobiles,_dobs,_states,_districts,_pincodes,_statuses=contract.functions.viewUsers().call()
    data=[]
    for i in range(len(_names)):
        if _statuses[i]==0 or _statuses[i]==1:
            dummy=[]
            dummy.append(_names[i])
            dummy.append(_adhars[i])
            dummy.append(_mobiles[i])
            dummy.append(_dobs[i])
            dummy.append(_states[i])
            dummy.append(_districts[i])
            dummy.append(_pincodes[i])
            if(_statuses[i]==0):
                dummy.append('Not Voted')
            elif(_statuses[i]==1):
                dummy.append('Voted')
            data.append(dummy)
    return render_template('data1.html',dashboard_data=data,l=len(data))

@app.route('/signupform',methods=['post'])
def signupform():
    name=request.form['name']
    aadhar=request.form['aadhar']
    aadhar1=request.form['aadhar1']
    mobile=request.form['mobile']
    dob=request.form['dob']
    state=request.form['state']
    district=request.form['district']
    pincode=request.form['pincode']
    print(name,aadhar,mobile,dob,state,district,pincode)

    if(aadhar!=aadhar1):
        return render_template('index.html',err='Aadhar Numbers didnt matched')
    if(len(aadhar)<12):
        return render_template('index.html',err='Aadhar number must be 12 digits long.')
    if(len(mobile)<10):
        return render_template('index.html',err='Mobile Num should be 10 digits')
    if(len(pincode)<6):
        return render_template('index.html',err='Pin Code should be 6 digits')

    try:
        contract,web3=connect_with_register()
        tx_hash=contract.functions.addUser(name,aadhar,mobile,dob,state,district,pincode).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return redirect('/login')
    except:
        return render_template('index.html',err='Cant signup')

@app.route('/login')
def loginPage():
    return render_template('Aadhar.html')

@app.route('/logindashboard', methods=['get','post'])
def logindashboard():
    aadhar=request.args.get('aadhar')
    mobile=request.args.get('mobile')
    print(aadhar,mobile)
    contract,web3=connect_with_register()
    _names,_adhars,_mobiles,_dobs,_states,_districts,_pincodes,_statuses=contract.functions.viewUsers().call()
    for i in range(len(_adhars)):
        if _adhars[i]==aadhar and _mobiles[i]==mobile:
            return redirect('/dashboard?adhar=aadhar')
    return render_template('Aadhar.html',err='Register First')


@app.route('/evaluateForm',methods=['post'])
def evaluateForm():
    aadhar=request.form['aadhar']
    contract,web3=connect_with_register()
    _names,_adhars,_mobiles,_dobs,_states,_districts,_pincodes,_statuses=contract.functions.viewUsers().call()
    print(_adhars)
    for i in _adhars:
        if i==aadhar:
            return render_template('login.html')
    else:
        return render_template('Aadhar.html',err='Register First')

@app.route('/dashboard',methods=['get'])
def dashboardPage():
    adhar=request.args.get('adhar')
    print(adhar)
    session['username']=adhar
    contract,web3=connect_with_voting()
    _votes=contract.functions.displayVotes().call()
    return render_template('dashboard.html',dashboard_data=_votes)

@app.route('/vote/<id>',methods=['get'])
def vote(id):
    print(id)
    try:
        contract,web3=connect_with_voting()
        tx_hash=contract.functions.castVote(int(id),session['username']).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        contract,web3=connect_with_register()
        tx_hash=contract.functions.validateUser(session['username'],1).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        contract,web3=connect_with_voting()
        _votes=contract.functions.displayVotes().call()
        return render_template('dashboard.html',res='vote casted',dashboard_data=_votes)
    except:
        contract,web3=connect_with_voting()
        _votes=contract.functions.displayVotes().call()
        return render_template('dashboard.html',err='volte already casted',dashboard_data=_votes)

@app.route('/logout')
def logout():
    session['username']=None
    return redirect('/')

if __name__=="__main__":
    app.run('0.0.0.0',port=5001,debug=True)