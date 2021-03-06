# -*- coding: UTF-8
#   Requests
#   ********
# 
# This file contain the specification of all the requests that can be made by a
# GLClient to a GLBackend.
# These specifications may be used with rest.validateMessage() inside of the
# handler to verify if the request is correct.

from globaleaks.rest.base import submissionGUS, GLTypes, formFieldsDict, contextGUS,\
    timeType, receiverGUS, fileGUS, profileGUS, tipGUS

class wbSubmissionDesc(GLTypes):

    specification = {
        'submission_gus': submissionGUS,
        'fields' : dict,
        'context_gus' : contextGUS,
        'creation_time' : timeType,
        'expiration_time' : timeType,
        'receivers' : [ receiverGUS ],
        'files' : [ fileGUS ],
        'receipt' : unicode,
        'finalize' : bool
    }

class receiverReceiverDesc(GLTypes):

    specification =  {
        'receiver_gus' : receiverGUS,
        'name' : unicode,
        'description' : unicode,
        'tags': list,
        'languages' : list,
        'creation_date' : timeType,
        'update_date' : timeType,
        'last_access' : timeType,
        'contexts' : [ contextGUS ],
        'receiver_level' : int,
        'can_delete_submission' : bool,
        'can_postpone_expiration' : bool,
        'can_configure_delivery' : bool,
        'can_configure_notification' : bool
    }

class receiverTipDesc(GLTypes):

    specification = {
        'tip_gus' : tipGUS,
        'notification_status' : unicode,
        'notification_date' : timeType,
        'last_access' : timeType,
        'access_counter' : int,
        'expressed_pertinence': int,
        'authoptions' : unicode,
    }

class actorsCommentDesc(GLTypes):

    specification = {
        'source' : unicode,
        'content' : unicode,
        'author' : unicode,
        'creation_time' : timeType
    }

class actorsTipOpsDesc(GLTypes):

    specification = {
        'personal_delete' : bool,
        'is_pertinent': bool
    }

class adminNodeDesc(GLTypes):

    specification = {
        'name': unicode,
        'description' : unicode,
        'hidden_service' : unicode,
        'public_site' : unicode,
        'public_stats_update_time' : int,
        'private_stats_update_time' : int,
        'email' : unicode,
        'languages' : list
    }

class adminContextDesc(GLTypes):

    specification = {
        'context_gus': contextGUS,
        'name': unicode,
        'description': unicode,
        'selectable_receiver': bool,
        'languages': list,
        'tip_max_access' : int,
        'tip_timetolive' : int,
        'file_max_download' : int,
        'escalation_threshold' : int,
        'receivers' : [ receiverGUS ],
        'fields': [ formFieldsDict ]
    }

class adminReceiverDesc(GLTypes):

    specification =  {
        'receiver_gus' : receiverGUS,
        'name' : unicode,
        'description' : unicode,
        'tags': list,
        'languages' : list,
        'creation_date' : timeType,
        'update_date' : timeType,
        'last_access' : timeType,
        'contexts' : [ contextGUS ],
        'receiver_level' : int,
        'notification_selected' : unicode,
        'notification_fields' : unicode,
        'delivery_selected' : unicode,
        'delivery_fields' : unicode,
        'can_delete_submission' : bool,
        'can_postpone_expiration' : bool,
        'can_configure_delivery' : bool,
        'can_configure_notification' : bool
    }

class adminProfileDesc(GLTypes):

    specification = {
        'plugin_type': unicode,
        'plugin_name' : unicode,
        'plugin_description' : unicode,
        'context_gus' : contextGUS,
        'profile_gus' : profileGUS,
        'profile_name' : unicode,
        'profile_description' : unicode,
        'creation_time' : timeType,
        'admin_fields' : [ formFieldsDict ],
        'admin_settings' : dict,
        'receiver_fields' : [ formFieldsDict ]
    }

class receiverConfDesc(GLTypes):

    specification = {
        'active' : bool,
        'config_id' : int,
        'receiver_settings' : dict,
        'creator_receiver' : receiverGUS,
        'context_gus' : contextGUS,
        'profile_gus' : profileGUS,
        'creation_date': timeType,
        'last_update': timeType
    }

