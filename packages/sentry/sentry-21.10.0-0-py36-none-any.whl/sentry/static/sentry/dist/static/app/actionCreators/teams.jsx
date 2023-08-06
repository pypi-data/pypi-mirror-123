Object.defineProperty(exports, "__esModule", { value: true });
exports.removeTeam = exports.createTeam = exports.leaveTeam = exports.joinTeam = exports.updateTeam = exports.updateTeamSuccess = exports.fetchTeamDetails = exports.fetchUserTeams = exports.fetchTeams = void 0;
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const teamActions_1 = (0, tslib_1.__importDefault)(require("app/actions/teamActions"));
const locale_1 = require("app/locale");
const callIfFunction_1 = require("app/utils/callIfFunction");
const guid_1 = require("app/utils/guid");
const doCallback = (params = {}, name, ...args) => {
    (0, callIfFunction_1.callIfFunction)(params[name], ...args);
};
// Fetch teams for org
function fetchTeams(api, params, options) {
    teamActions_1.default.fetchAll(params.orgId);
    return api.request(`/teams/${params.orgId}/`, {
        success: data => {
            teamActions_1.default.fetchAllSuccess(params.orgId, data);
            doCallback(options, 'success', data);
        },
        error: error => {
            teamActions_1.default.fetchAllError(params.orgId, error);
            doCallback(options, 'error', error);
        },
    });
}
exports.fetchTeams = fetchTeams;
// Fetch user teams for current org and place them in the team store
function fetchUserTeams(api, params) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const teams = yield api.requestPromise(`/organizations/${params.orgId}/user-teams/`);
        teamActions_1.default.loadUserTeams(teams);
    });
}
exports.fetchUserTeams = fetchUserTeams;
function fetchTeamDetails(api, params, options) {
    teamActions_1.default.fetchDetails(params.teamId);
    return api.request(`/teams/${params.orgId}/${params.teamId}/`, {
        success: data => {
            teamActions_1.default.fetchDetailsSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: error => {
            teamActions_1.default.fetchDetailsError(params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
exports.fetchTeamDetails = fetchTeamDetails;
function updateTeamSuccess(teamId, data) {
    teamActions_1.default.updateSuccess(teamId, data);
}
exports.updateTeamSuccess = updateTeamSuccess;
function updateTeam(api, params, options) {
    const endpoint = `/teams/${params.orgId}/${params.teamId}/`;
    teamActions_1.default.update(params.teamId, params.data);
    return api.request(endpoint, {
        method: 'PUT',
        data: params.data,
        success: data => {
            updateTeamSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: error => {
            teamActions_1.default.updateError(params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
exports.updateTeam = updateTeam;
function joinTeam(api, params, options) {
    var _a;
    const endpoint = `/organizations/${params.orgId}/members/${(_a = params.memberId) !== null && _a !== void 0 ? _a : 'me'}/teams/${params.teamId}/`;
    const id = (0, guid_1.uniqueId)();
    teamActions_1.default.update(id, params.teamId);
    return api.request(endpoint, {
        method: 'POST',
        success: data => {
            teamActions_1.default.updateSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: error => {
            teamActions_1.default.updateError(id, params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
exports.joinTeam = joinTeam;
function leaveTeam(api, params, options) {
    const endpoint = `/organizations/${params.orgId}/members/${params.memberId || 'me'}/teams/${params.teamId}/`;
    const id = (0, guid_1.uniqueId)();
    teamActions_1.default.update(id, params.teamId);
    return api.request(endpoint, {
        method: 'DELETE',
        success: data => {
            teamActions_1.default.updateSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: error => {
            teamActions_1.default.updateError(id, params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
exports.leaveTeam = leaveTeam;
function createTeam(api, team, params) {
    teamActions_1.default.createTeam(team);
    return api
        .requestPromise(`/organizations/${params.orgId}/teams/`, {
        method: 'POST',
        data: team,
    })
        .then(data => {
        teamActions_1.default.createTeamSuccess(data);
        (0, indicator_1.addSuccessMessage)((0, locale_1.tct)('[team] has been added to the [organization] organization', {
            team: `#${data.slug}`,
            organization: params.orgId,
        }));
        return data;
    }, err => {
        teamActions_1.default.createTeamError(team.slug, err);
        (0, indicator_1.addErrorMessage)((0, locale_1.tct)('Unable to create [team] in the [organization] organization', {
            team: `#${team.slug}`,
            organization: params.orgId,
        }));
        throw err;
    });
}
exports.createTeam = createTeam;
function removeTeam(api, params) {
    teamActions_1.default.removeTeam(params.teamId);
    return api
        .requestPromise(`/teams/${params.orgId}/${params.teamId}/`, {
        method: 'DELETE',
    })
        .then(data => {
        teamActions_1.default.removeTeamSuccess(params.teamId, data);
        (0, indicator_1.addSuccessMessage)((0, locale_1.tct)('[team] has been removed from the [organization] organization', {
            team: `#${params.teamId}`,
            organization: params.orgId,
        }));
        return data;
    }, err => {
        teamActions_1.default.removeTeamError(params.teamId, err);
        (0, indicator_1.addErrorMessage)((0, locale_1.tct)('Unable to remove [team] from the [organization] organization', {
            team: `#${params.teamId}`,
            organization: params.orgId,
        }));
        throw err;
    });
}
exports.removeTeam = removeTeam;
//# sourceMappingURL=teams.jsx.map