Object.defineProperty(exports, "__esModule", { value: true });
exports.mergeGroups = exports.bulkUpdate = exports.bulkDelete = exports.paramsToQueryArgs = exports.updateNote = exports.createNote = exports.deleteNote = exports.assignToActor = exports.clearAssignment = exports.assignToUser = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const isNil_1 = (0, tslib_1.__importDefault)(require("lodash/isNil"));
const groupActions_1 = (0, tslib_1.__importDefault)(require("app/actions/groupActions"));
const api_1 = require("app/api");
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const utils_1 = require("app/utils");
const guid_1 = require("app/utils/guid");
function assignToUser(params) {
    const api = new api_1.Client();
    const endpoint = `/issues/${params.id}/`;
    const id = (0, guid_1.uniqueId)();
    groupActions_1.default.assignTo(id, params.id, {
        email: (params.member && params.member.email) || '',
    });
    const request = api.requestPromise(endpoint, {
        method: 'PUT',
        // Sending an empty value to assignedTo is the same as "clear",
        // so if no member exists, that implies that we want to clear the
        // current assignee.
        data: {
            assignedTo: params.user ? (0, utils_1.buildUserId)(params.user.id) : '',
            assignedBy: params.assignedBy,
        },
    });
    request
        .then(data => {
        groupActions_1.default.assignToSuccess(id, params.id, data);
    })
        .catch(data => {
        groupActions_1.default.assignToError(id, params.id, data);
    });
    return request;
}
exports.assignToUser = assignToUser;
function clearAssignment(groupId, assignedBy) {
    const api = new api_1.Client();
    const endpoint = `/issues/${groupId}/`;
    const id = (0, guid_1.uniqueId)();
    groupActions_1.default.assignTo(id, groupId, {
        email: '',
    });
    const request = api.requestPromise(endpoint, {
        method: 'PUT',
        // Sending an empty value to assignedTo is the same as "clear"
        data: {
            assignedTo: '',
            assignedBy,
        },
    });
    request
        .then(data => {
        groupActions_1.default.assignToSuccess(id, groupId, data);
    })
        .catch(data => {
        groupActions_1.default.assignToError(id, groupId, data);
    });
    return request;
}
exports.clearAssignment = clearAssignment;
function assignToActor({ id, actor, assignedBy }) {
    const api = new api_1.Client();
    const endpoint = `/issues/${id}/`;
    const guid = (0, guid_1.uniqueId)();
    let actorId;
    groupActions_1.default.assignTo(guid, id, { email: '' });
    switch (actor.type) {
        case 'user':
            actorId = (0, utils_1.buildUserId)(actor.id);
            break;
        case 'team':
            actorId = (0, utils_1.buildTeamId)(actor.id);
            break;
        default:
            Sentry.withScope(scope => {
                scope.setExtra('actor', actor);
                Sentry.captureException('Unknown assignee type');
            });
    }
    return api
        .requestPromise(endpoint, {
        method: 'PUT',
        data: { assignedTo: actorId, assignedBy },
    })
        .then(data => {
        groupActions_1.default.assignToSuccess(guid, id, data);
    })
        .catch(data => {
        groupActions_1.default.assignToError(guid, id, data);
    });
}
exports.assignToActor = assignToActor;
function deleteNote(api, group, id, _oldText) {
    const restore = group.activity.find(activity => activity.id === id);
    const index = groupStore_1.default.removeActivity(group.id, id);
    if (index === -1) {
        // I dunno, the id wasn't found in the GroupStore
        return Promise.reject(new Error('Group was not found in store'));
    }
    const promise = api.requestPromise(`/issues/${group.id}/comments/${id}/`, {
        method: 'DELETE',
    });
    promise.catch(() => groupStore_1.default.addActivity(group.id, restore, index));
    return promise;
}
exports.deleteNote = deleteNote;
function createNote(api, group, note) {
    const promise = api.requestPromise(`/issues/${group.id}/comments/`, {
        method: 'POST',
        data: note,
    });
    promise.then(data => groupStore_1.default.addActivity(group.id, data));
    return promise;
}
exports.createNote = createNote;
function updateNote(api, group, note, id, oldText) {
    groupStore_1.default.updateActivity(group.id, id, { text: note.text });
    const promise = api.requestPromise(`/issues/${group.id}/comments/${id}/`, {
        method: 'PUT',
        data: note,
    });
    promise.catch(() => groupStore_1.default.updateActivity(group.id, id, { text: oldText }));
    return promise;
}
exports.updateNote = updateNote;
/**
 * Converts input parameters to API-compatible query arguments
 */
function paramsToQueryArgs(params) {
    var _a;
    const p = params.itemIds
        ? { id: params.itemIds } // items matching array of itemids
        : params.query
            ? { query: params.query } // items matching search query
            : {}; // all items
    // only include environment if it is not null/undefined
    if (params.query && !(0, isNil_1.default)(params.environment)) {
        p.environment = params.environment;
    }
    // only include projects if it is not null/undefined/an empty array
    if ((_a = params.project) === null || _a === void 0 ? void 0 : _a.length) {
        p.project = params.project;
    }
    // only include date filters if they are not null/undefined
    if (params.query) {
        ['start', 'end', 'period', 'utc'].forEach(prop => {
            if (!(0, isNil_1.default)(params[prop])) {
                p[prop === 'period' ? 'statsPeriod' : prop] = params[prop];
            }
        });
    }
    return p;
}
exports.paramsToQueryArgs = paramsToQueryArgs;
function getUpdateUrl({ projectId, orgId }) {
    return projectId
        ? `/projects/${orgId}/${projectId}/issues/`
        : `/organizations/${orgId}/issues/`;
}
function chainUtil(...funcs) {
    const filteredFuncs = funcs.filter((f) => typeof f === 'function');
    return (...args) => {
        filteredFuncs.forEach(func => {
            func.apply(funcs, args);
        });
    };
}
function wrapRequest(api, path, options, extraParams = {}) {
    options.success = chainUtil(options.success, extraParams.success);
    options.error = chainUtil(options.error, extraParams.error);
    options.complete = chainUtil(options.complete, extraParams.complete);
    return api.request(path, options);
}
function bulkDelete(api, params, options) {
    const { itemIds } = params;
    const path = getUpdateUrl(params);
    const query = paramsToQueryArgs(params);
    const id = (0, guid_1.uniqueId)();
    groupActions_1.default.delete(id, itemIds);
    return wrapRequest(api, path, {
        query,
        method: 'DELETE',
        success: response => {
            groupActions_1.default.deleteSuccess(id, itemIds, response);
        },
        error: error => {
            groupActions_1.default.deleteError(id, itemIds, error);
        },
    }, options);
}
exports.bulkDelete = bulkDelete;
function bulkUpdate(api, params, options) {
    const { itemIds, failSilently, data } = params;
    const path = getUpdateUrl(params);
    const query = paramsToQueryArgs(params);
    const id = (0, guid_1.uniqueId)();
    groupActions_1.default.update(id, itemIds, data);
    return wrapRequest(api, path, {
        query,
        method: 'PUT',
        data,
        success: response => {
            groupActions_1.default.updateSuccess(id, itemIds, response);
        },
        error: error => {
            groupActions_1.default.updateError(id, itemIds, error, failSilently);
        },
    }, options);
}
exports.bulkUpdate = bulkUpdate;
function mergeGroups(api, params, options) {
    const { itemIds } = params;
    const path = getUpdateUrl(params);
    const query = paramsToQueryArgs(params);
    const id = (0, guid_1.uniqueId)();
    groupActions_1.default.merge(id, itemIds);
    return wrapRequest(api, path, {
        query,
        method: 'PUT',
        data: { merge: 1 },
        success: response => {
            groupActions_1.default.mergeSuccess(id, itemIds, response);
        },
        error: error => {
            groupActions_1.default.mergeError(id, itemIds, error);
        },
    }, options);
}
exports.mergeGroups = mergeGroups;
//# sourceMappingURL=group.jsx.map