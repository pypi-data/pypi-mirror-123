Object.defineProperty(exports, "__esModule", { value: true });
exports.toggleKeyTransaction = exports.fetchTeamKeyTransactions = void 0;
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
const parseLinkHeader_1 = (0, tslib_1.__importDefault)(require("app/utils/parseLinkHeader"));
function fetchTeamKeyTransactions(api, orgSlug, teams, projects) {
    var _a, _b, _c, _d, _e, _f;
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const url = `/organizations/${orgSlug}/key-transactions-list/`;
        const datas = [];
        let cursor = undefined;
        let hasMore = true;
        while (hasMore) {
            try {
                const payload = { cursor, team: teams, project: projects };
                if (!payload.cursor) {
                    delete payload.cursor;
                }
                if (!((_a = payload.project) === null || _a === void 0 ? void 0 : _a.length)) {
                    delete payload.project;
                }
                const [data, , resp] = yield api.requestPromise(url, {
                    method: 'GET',
                    includeAllArgs: true,
                    query: payload,
                });
                datas.push(data);
                const pageLinks = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link');
                if (pageLinks) {
                    const paginationObject = (0, parseLinkHeader_1.default)(pageLinks);
                    hasMore = (_c = (_b = paginationObject === null || paginationObject === void 0 ? void 0 : paginationObject.next) === null || _b === void 0 ? void 0 : _b.results) !== null && _c !== void 0 ? _c : false;
                    cursor = (_d = paginationObject.next) === null || _d === void 0 ? void 0 : _d.cursor;
                }
                else {
                    hasMore = false;
                }
            }
            catch (err) {
                (0, indicator_1.addErrorMessage)((_f = (_e = err.responseJSON) === null || _e === void 0 ? void 0 : _e.detail) !== null && _f !== void 0 ? _f : (0, locale_1.t)('Error fetching team key transactions'));
                throw err;
            }
        }
        return datas.flat();
    });
}
exports.fetchTeamKeyTransactions = fetchTeamKeyTransactions;
function toggleKeyTransaction(api, isKeyTransaction, orgId, projects, transactionName, teamIds // TODO(txiao): make this required
) {
    (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving changes\u2026'));
    const promise = api.requestPromise(`/organizations/${orgId}/key-transactions/`, {
        method: isKeyTransaction ? 'DELETE' : 'POST',
        query: {
            project: projects.map(id => String(id)),
        },
        data: {
            transaction: transactionName,
            team: teamIds,
        },
    });
    promise.then(indicator_1.clearIndicators);
    promise.catch(response => {
        var _a;
        const responseJSON = response === null || response === void 0 ? void 0 : response.responseJSON;
        const errorDetails = (_a = responseJSON === null || responseJSON === void 0 ? void 0 : responseJSON.detail) !== null && _a !== void 0 ? _a : responseJSON === null || responseJSON === void 0 ? void 0 : responseJSON.non_field_errors;
        if (Array.isArray(errorDetails) && errorDetails.length && errorDetails[0]) {
            (0, indicator_1.addErrorMessage)(errorDetails[0]);
        }
        else {
            (0, indicator_1.addErrorMessage)(errorDetails !== null && errorDetails !== void 0 ? errorDetails : (0, locale_1.t)('Unable to update key transaction'));
        }
    });
    return promise;
}
exports.toggleKeyTransaction = toggleKeyTransaction;
//# sourceMappingURL=performance.jsx.map