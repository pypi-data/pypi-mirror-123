Object.defineProperty(exports, "__esModule", { value: true });
exports.getLabel = exports.getConfirm = exports.ConfirmAction = exports.BULK_LIMIT_STR = exports.BULK_LIMIT = void 0;
const tslib_1 = require("tslib");
const capitalize_1 = (0, tslib_1.__importDefault)(require("lodash/capitalize"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const extraDescription_1 = (0, tslib_1.__importDefault)(require("./extraDescription"));
exports.BULK_LIMIT = 1000;
exports.BULK_LIMIT_STR = exports.BULK_LIMIT.toLocaleString();
var ConfirmAction;
(function (ConfirmAction) {
    ConfirmAction["RESOLVE"] = "resolve";
    ConfirmAction["UNRESOLVE"] = "unresolve";
    ConfirmAction["IGNORE"] = "ignore";
    ConfirmAction["BOOKMARK"] = "bookmark";
    ConfirmAction["UNBOOKMARK"] = "unbookmark";
    ConfirmAction["MERGE"] = "merge";
    ConfirmAction["DELETE"] = "delete";
})(ConfirmAction = exports.ConfirmAction || (exports.ConfirmAction = {}));
function getBulkConfirmMessage(action, queryCount) {
    if (queryCount > exports.BULK_LIMIT) {
        return (0, locale_1.tct)('Are you sure you want to [action] the first [bulkNumber] issues that match the search?', {
            action,
            bulkNumber: exports.BULK_LIMIT_STR,
        });
    }
    return (0, locale_1.tct)('Are you sure you want to [action] all [bulkNumber] issues that match the search?', {
        action,
        bulkNumber: queryCount,
    });
}
function getConfirm(numIssues, allInQuerySelected, query, queryCount) {
    return function (action, canBeUndone, append = '') {
        const question = allInQuerySelected
            ? getBulkConfirmMessage(`${action}${append}`, queryCount)
            : (0, locale_1.tn)(`Are you sure you want to ${action} this %s issue${append}?`, `Are you sure you want to ${action} these %s issues${append}?`, numIssues);
        let message;
        switch (action) {
            case ConfirmAction.DELETE:
                message = (0, locale_1.tct)('Bulk deletion is only recommended for junk data. To clear your stream, consider resolving or ignoring. [link:When should I delete events?]', {
                    link: (<externalLink_1.default href="https://help.sentry.io/account/billing/when-should-i-delete-events/"/>),
                });
                break;
            case ConfirmAction.MERGE:
                message = (0, locale_1.t)('Note that unmerging is currently an experimental feature.');
                break;
            default:
                message = (0, locale_1.t)('This action cannot be undone.');
        }
        return (<div>
        <p style={{ marginBottom: '20px' }}>
          <strong>{question}</strong>
        </p>
        <extraDescription_1.default all={allInQuerySelected} query={query} queryCount={queryCount}/>
        {!canBeUndone && <p>{message}</p>}
      </div>);
    };
}
exports.getConfirm = getConfirm;
function getLabel(numIssues, allInQuerySelected) {
    return function (action, append = '') {
        const capitalized = (0, capitalize_1.default)(action);
        const text = allInQuerySelected
            ? (0, locale_1.t)(`Bulk ${action} issues`)
            : (0, locale_1.tn)(`${capitalized} %s selected issue`, `${capitalized} %s selected issues`, numIssues);
        return text + append;
    };
}
exports.getLabel = getLabel;
//# sourceMappingURL=utils.jsx.map