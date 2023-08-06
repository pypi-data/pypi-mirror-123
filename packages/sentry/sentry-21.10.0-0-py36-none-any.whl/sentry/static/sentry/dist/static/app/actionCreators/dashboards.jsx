Object.defineProperty(exports, "__esModule", { value: true });
exports.validateWidget = exports.deleteDashboard = exports.updateDashboard = exports.fetchDashboard = exports.updateDashboardVisit = exports.createDashboard = void 0;
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
function createDashboard(api, orgId, newDashboard, duplicate) {
    const { title, widgets } = newDashboard;
    const promise = api.requestPromise(`/organizations/${orgId}/dashboards/`, {
        method: 'POST',
        data: { title, widgets, duplicate },
    });
    promise.catch(response => {
        var _a;
        const errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            (0, indicator_1.addErrorMessage)(errorResponse);
        }
        else {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to create dashboard'));
        }
    });
    return promise;
}
exports.createDashboard = createDashboard;
function updateDashboardVisit(api, orgId, dashboardId) {
    const promise = api.requestPromise(`/organizations/${orgId}/dashboards/${dashboardId}/visit/`, {
        method: 'POST',
    });
    return promise;
}
exports.updateDashboardVisit = updateDashboardVisit;
function fetchDashboard(api, orgId, dashboardId) {
    const promise = api.requestPromise(`/organizations/${orgId}/dashboards/${dashboardId}/`, {
        method: 'GET',
    });
    promise.catch(response => {
        var _a;
        const errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            (0, indicator_1.addErrorMessage)(errorResponse);
        }
        else {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to load dashboard'));
        }
    });
    return promise;
}
exports.fetchDashboard = fetchDashboard;
function updateDashboard(api, orgId, dashboard) {
    const data = {
        title: dashboard.title,
        widgets: dashboard.widgets,
    };
    const promise = api.requestPromise(`/organizations/${orgId}/dashboards/${dashboard.id}/`, {
        method: 'PUT',
        data,
    });
    promise.catch(response => {
        var _a;
        const errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            (0, indicator_1.addErrorMessage)(errorResponse);
        }
        else {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to update dashboard'));
        }
    });
    return promise;
}
exports.updateDashboard = updateDashboard;
function deleteDashboard(api, orgId, dashboardId) {
    const promise = api.requestPromise(`/organizations/${orgId}/dashboards/${dashboardId}/`, {
        method: 'DELETE',
    });
    promise.catch(response => {
        var _a;
        const errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            (0, indicator_1.addErrorMessage)(errorResponse);
        }
        else {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to delete dashboard'));
        }
    });
    return promise;
}
exports.deleteDashboard = deleteDashboard;
function validateWidget(api, orgId, widget) {
    const promise = api.requestPromise(`/organizations/${orgId}/dashboards/widgets/`, {
        method: 'POST',
        data: widget,
    });
    return promise;
}
exports.validateWidget = validateWidget;
//# sourceMappingURL=dashboards.jsx.map