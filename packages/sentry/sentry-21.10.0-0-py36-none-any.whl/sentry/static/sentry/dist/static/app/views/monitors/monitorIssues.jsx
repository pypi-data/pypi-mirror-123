Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const issueList_1 = (0, tslib_1.__importDefault)(require("app/components/issueList"));
const locale_1 = require("app/locale");
const MonitorIssues = ({ orgId, monitor }) => (<issueList_1.default endpoint={`/organizations/${orgId}/issues/`} query={{
        query: 'monitor.id:"' + monitor.id + '"',
        project: monitor.project.id,
        limit: 5,
    }} pagination={false} emptyText={(0, locale_1.t)('No issues found')} noBorder noMargin/>);
exports.default = MonitorIssues;
//# sourceMappingURL=monitorIssues.jsx.map