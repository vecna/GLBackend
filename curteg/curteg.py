#!/usr/bin/python
import httplib, json
import sys, os, time

cwd = '/'.join(__file__.split('/')[:-1])
sys.path.insert(0, os.path.join(cwd, '../'))

from globaleaks.utils.idops import random_submission_id
from globaleaks.utils.idops import random_tip_id
from globaleaks.utils.idops import random_context_id

from globaleaks.rest import answers
from globaleaks.rest import requests
from globaleaks.utils.dummy import dummy_answers
from globaleaks.utils.dummy import dummy_requests
from globaleaks.utils import recurringtypes

# U1 `/node/`
# U2 `/submission`
# U3 `/submission/<submission_id>`
# U4 `/submission/<submission_id>/finalize`
# U5 `/submission/<submission_id>/upload_file`

# R1 `/receiver/<string t_id>/overview`
# R2 `/receiver/<string module_name><string t_id>/module`

# A1 `/admin/node/`
# A2 `/admin/contexts/`
# A3 `/admin/receivers/<context_$ID>/`
# A4 `/admin/modules/<context_$ID>/<string module_type>/`

# T1 `/tip/<string auth t_id>`
# T2 `/tip/<uniq_Tip_$ID>/add_comment`
# T3 `/tip/<uniq_Tip_$ID>/update_file`
# T4 `/tip/<string t_id>/finalize_update`
# T5 `/tip/<string t_id>/download_material`
# T6 `/tip/<string t_id>/pertinence`

# https://github.com/globaleaks/GlobaLeaks/wiki/API-Specification
# https://github.com/globaleaks/GlobaLeaks/wiki/recurring-data-types


def checkOpt(option):

    if option in sys.argv:
        return True

    if option in [ 'requests', 'response' ] and 'verbose' in sys.argv:
        return True

    return False

def get_parm(keyword):

    for i, arg in enumerate(sys.argv):
        if arg == keyword:

            hooked = sys.argv[i + 1]
            if checkOpt('verbose'):
                print "using as", keyword, hooked

            return hooked

"""
Context, Submission and Tip shall be passed via command line, using the
optios 'sid' 'tid' and 'cid'
"""
def sID():
    if checkOpt('sid'):
        return get_parm('sid')
    else:
        return random_submission_id()

def tID():
    if checkOpt('tid'):
        return get_parm('tid')
    else:
        return random_tip_id()

def cID():
    if checkOpt('cid'):
        return get_parm('cid')
    else:
        return random_context_id()


"""
Request schema,
linking the identificative synthesis, the URL, the method
"""
schema = {
     "U1" :['/node', {
            'GET' : [
            False, False, answers.nodeMainSettings
         ] } ],
     "U2" :['/submission', {
            'GET': [
            False, False, answers.newSubmission
         ] } ],
     "U3" :['/submission/'+sID()+'/status', {
          'GET' : [
            False, False, answers.submissionStatus ],
          'POST' : [
            requests.submissionUpdate,
            dummy_requests.SUBMISSION_STATUS_POST,
            answers.submissionStatus
         ] } ],
     "U4" :['/submission/'+sID()+'/finalize', {
         'POST': [
            requests.finalizeSubmission,
            dummy_requests.SUBMISSION_FINALIZE_POST,
            answers.finalizeSubmission
         ] } ],
     # "U5" :['/submission/'+sID()+'/files', ['GET','POST','PUT','DELETE']],
     "T1" :['/tip/', {
         'GET' : [
             False, False, recurringtypes.tipDetailsDict ],
         'POST' : [
             requests.tipOperations,
             dummy_requests.TIP_OPTIONS_POST,
             False
         ] } ],
     "T2" :['/tip/'+tID()+'/comment', {
         'POST' : [
             requests.sendComment,
             dummy_requests.TIP_COMMENT_POST,
             False
         ] } ],
     # "T3" :['/tip/'+tID()+'/files', ['GET','POST','PUT','DELETE']],
     "T4" :['/tip/'+tID()+'/finalize', {
         'POST' : [
             requests.finalizeIntegration,
             dummy_requests.TIP_FINALIZE_POST,
             False
         ] } ],
     "T5" :['/tip/'+tID()+'/download', {
         'GET' : [
             False, False, False
         ] } ],
     "T6" :['/tip/'+tID()+'/pertinence', { 
         'POST' : [
             requests.pertinenceVote,
             dummy_requests.TIP_PERTINENCE_POST,
             False
         ] } ],
     "R1" :['/receiver/' + tID(), {
         'GET' : [
             False, False, answers.commonReceiverAnswer
         ] } ],
     "R2" :['/receiver/' + tID() +'/notification', {
         'GET' : [
             False, False, answers.receiverModuleAnswer ],
         'POST' : [
             requests.receiverOptions,
             dummy_requests.RECEIVER_MODULE_POST,
             answers.receiverModuleAnswer ],
         'PUT' : [
             requests.receiverOptions,
             dummy_requests.RECEIVER_MODULE_PUT,
             answers.receiverModuleAnswer ],
         'DELETE' : [
             requests.receiverOptions,
             dummy_requests.RECEIVER_MODULE_DELETE,
             answers. receiverModuleAnswer
         ] } ],
     "A1" :['/admin/node', {
         'GET' : [
             False, False, answers.nodeMainSettings ],
         'POST' : [
             requests.nodeAdminSetup,
             dummy_requests.ADMIN_NODE_POST,
             answers.nodeMainSettings
         ] } ],
     "A2" :['/admin/contexts/' + cID(), {
         'GET' : [
             False, False, answers.adminContextsCURD ],
         'POST' : [
             requests.contextConfiguration,
             dummy_requests.ADMIN_CONTEXTS_POST,
             answers.adminContextsCURD ],
         'PUT' : [
             requests.contextConfiguration,
             dummy_requests.ADMIN_CONTEXTS_PUT,
             answers.adminContextsCURD ],
         'DELETE' : [
             requests.contextConfiguration,
             dummy_requests.ADMIN_CONTEXTS_DELETE,
             answers.adminContextsCURD
         ] } ],
     "A3" :['/admin/receivers/' +cID(), {
         'GET' : [
             False, False, answers.adminReceiverCURD ],
         'POST' : [
             requests.receiverConfiguration,
             dummy_requests.ADMIN_RECEIVERS_POST,
             answers.adminReceiverCURD ],
         'PUT' : [
             requests.receiverConfiguration,
             dummy_requests.ADMIN_RECEIVERS_PUT,
             answers.adminReceiverCURD ],
         'DELETE' : [
             requests.receiverConfiguration,
             dummy_requests.ADMIN_RECEIVERS_DELETE,
             answers.adminReceiverCURD
         ] } ],
     "A4" :['/admin/modules/'+cID()+'/notification', {
         'GET' : [
             False, False, answers.adminModulesUR ],
         'POST' : [
             requests.moduleConfiguration,
             dummy_requests.ADMIN_MODULES_POST,
             answers.adminModulesUR
         ] } ]
}

baseurl = "127.0.0.1:8082"



"""
---------------- # ---------------
"""

def do_curl(url, method, not_encoded_parm=''):

    headers = {'Content-Type': 'application/json-rpc; charset=utf-8'}

    time.sleep(0.1)
    conn = httplib.HTTPConnection(baseurl)

    if checkOpt('request'):
        print "[+] CONNECTION REQUEST:", method, baseurl, url, not_encoded_parm, headers,"\n"

    params = json.dumps(not_encoded_parm, ensure_ascii=False)
    params.encode('utf-8')

    conn.request(method, url, params, headers)

    response = conn.getresponse()
    # response is an HTTPResponse instance

    received_data = response.read()
    if checkOpt('response'):
        print "[+] RESPONSE:", received_data,"\n"

    if response.status != 200:
        if response.status > 400: # client & server errors
            print "Error code", response.status
            print received_data
        else:
            # is one of the few 201 (Created) instead of 200 (OK)
            # is not printed for keep output clean and parsable
            pass

    if checkOpt('verbose'):
        print "Response status code:", response.status

    # as dict ? or need to be imported as json ?
    convertedInAdict = json.loads(received_data)
    # outputOptionsApply(dict(received_data))
    outputOptionsApply(convertedInAdict)

    conn.close()

    return received_data


"""
['/submission/s_LCjNrPCGDqeMbQaIUbNbKUPtrrDuArvkEMlSAUwduQgJewpIfR/status', {'POST': [<class
globaleaks.rest.requests.submissionUpdate at 0x224a0b8>, <function SUBMISSION_STATUS_POST at
0x2252050>], 'GET': None}]
"""
def handle_selected_test(keyapi):

    url = schema[keyapi][0]
    methodsAndFunctions = schema[keyapi][1]

    requestedMethods = []
    for meth in [ 'GET', 'POST', 'PUT', 'DELETE' ]:
        if checkOpt(meth):
            requestedMethods.append(meth)

    for method in methodsAndFunctions.iterkeys():
        if len(requestedMethods) > 0 and not (method in requestedMethods):
            continue

        if  methodsAndFunctions.get(method)[2]:
            answerGLT = methodsAndFunctions.get(method)[2]()
        else:
            answerGLT = None

        # GET has not a request, then
        if methodsAndFunctions.get(method)[0] == False:
            output = do_curl(url, method)
        else:
            # request generation: call globaleaks.rest.requests
            requestGLT = methodsAndFunctions.get(method)[0]()

            # request filling: call globaleaks.utils.dummy.dummy_requests
            methodsAndFunctions.get(method)[1](requestGLT)

            # requestGLT need to be .unroll() for be a dict
            request = requestGLT.unroll()

            # is input data exists, may be modified
            realRequest = inputOptionsApply(request)

            output = do_curl(url, method, realRequest)

        if answerGLT:

            if output:
                compare_output(output, answerGLT)
            else:
                print "Expected output, but not output received!"


def compare_output(received, expected):

    # TODO compare extending GLTypes
    if checkOpt('verbose'):
        print "received has", received, "expected", expected.unroll()


def inputOptionsApply(theDict):

    if checkOpt('hand'):
        import tempfile, os, pickle

        swaptname = tempfile.mkstemp('curteg', 'tmp', '/tmp/')[1]

        f = file(swaptname, 'w+')
        pickle.dump(theDict, f)
        f.close()

        os.system("vim " + swaptname)
        f = file(swaptname, 'r')
        theNewDict = pickle.load(f)
        f.close()

        return theNewDict

def outputOptionsApply(theDict):

    for uarg in sys.argv:
        if uarg.startswith('print-'):
            choosen = uarg[6:]

            if theDict.has_key(choosen):
                print theDict[choosen]
            else:
                print "requested key", choosen, "missing from the received data"


"""
---------------- # ---------------
"""

if __name__ != "__main__":
    print "compliment guy, you're using this test in a new way"
    raise Exception("we don't like innovation, bwahahah")

selective = False

if len(sys.argv) >= 2:
    for opt in enumerate(sys.argv):
        if opt[1].find(':') != -1:
            baseurl = x[1]
            print "switching test service to:", baseurl

        if len(opt[1]) == 2 and int(opt[1][1]) < 9:
            selective = True
            handle_selected_test(opt[1])

if not selective:
    for tests in schema.iterkeys():
        handle_selected_test(tests)
