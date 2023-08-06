Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
function ErrorMessage({ error, groupId, onRetry, orgSlug, projSlug, hasProjectWriteAccess, }) {
    var _a;
    function getErrorDetails(errorCode) {
        switch (errorCode) {
            case 'merged_issues':
                return {
                    title: (0, locale_1.t)('Grouping breakdown is not available in this issue'),
                    subTitle: (0, locale_1.t)('This issue needs to be fully unmerged before grouping breakdown is available'),
                    action: (<button_1.default priority="primary" to={`/organizations/sentry/issues/${groupId}/merged/?${location.search}`}>
              {(0, locale_1.t)('Unmerge issue')}
            </button_1.default>),
                };
            case 'missing_feature':
                return {
                    title: (0, locale_1.t)('This project does not have the grouping breakdown available. Is your organization still an early adopter?'),
                };
            case 'no_events':
                return {
                    title: (0, locale_1.t)('This issue has no events'),
                };
            case 'issue_not_hierarchical':
                return {
                    title: (0, locale_1.t)('Grouping breakdown is not available in this issue'),
                    subTitle: (0, locale_1.t)('Only new issues with the latest grouping strategy have this feature available'),
                };
            case 'project_not_hierarchical':
                return {
                    title: (<react_1.Fragment>
              {(0, locale_1.t)('Update your Grouping Config')}
              <featureBadge_1.default type="beta"/>
            </react_1.Fragment>),
                    subTitle: (<react_1.Fragment>
              <p>
                {(0, locale_1.t)('Enable advanced grouping insights and functionality by updating this project to the latest Grouping Config:')}
              </p>

              <ul>
                <li>
                  {(0, locale_1.tct)('[strong:Breakdowns:] Explore events in this issue by call hierarchy.', { strong: <strong /> })}
                </li>
                <li>
                  {(0, locale_1.tct)('[strong:Stack trace annotations:] See important frames Sentry uses to group issues directly in the stack trace.', { strong: <strong /> })}
                </li>
              </ul>
            </react_1.Fragment>),
                    leftAligned: true,
                    action: (<buttonBar_1.default gap={1}>
              <button_1.default priority="primary" to={`/settings/${orgSlug}/projects/${projSlug}/issue-grouping/#upgrade-grouping`} disabled={!hasProjectWriteAccess} title={!hasProjectWriteAccess
                            ? (0, locale_1.t)('You do not have permission to update this project')
                            : undefined}>
                {(0, locale_1.t)('Upgrade Grouping Strategy')}
              </button_1.default>
              <button_1.default href="https://docs.sentry.io/product/data-management-settings/event-grouping/grouping-breakdown/">
                {(0, locale_1.t)('Read the docs')}
              </button_1.default>
            </buttonBar_1.default>),
                };
            default:
                return {};
        }
    }
    if (typeof error === 'string') {
        return <alert_1.default type="warning">{error}</alert_1.default>;
    }
    if (error.status === 403 && ((_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail)) {
        const { code, message } = error.responseJSON.detail;
        const { action, title, subTitle, leftAligned } = getErrorDetails(code);
        return (<panels_1.Panel>
        <emptyMessage_1.default size="large" title={title !== null && title !== void 0 ? title : message} description={subTitle} action={action} leftAligned={leftAligned}/>
      </panels_1.Panel>);
    }
    return (<loadingError_1.default message={(0, locale_1.t)('Unable to load grouping levels, please try again later')} onRetry={onRetry}/>);
}
exports.default = ErrorMessage;
//# sourceMappingURL=errorMessage.jsx.map