Object.defineProperty(exports, "__esModule", { value: true });
exports.SentryAppExternalIssueForm = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const locale_1 = require("app/locale");
const externalIssueStore_1 = (0, tslib_1.__importDefault)(require("app/stores/externalIssueStore"));
const getStacktraceBody_1 = (0, tslib_1.__importDefault)(require("app/utils/getStacktraceBody"));
const queryString_1 = require("app/utils/queryString");
const sentryAppExternalForm_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/sentryAppExternalForm"));
class SentryAppExternalIssueForm extends react_1.Component {
    constructor() {
        super(...arguments);
        this.onSubmitSuccess = (issue) => {
            externalIssueStore_1.default.add(issue);
            this.props.onSubmitSuccess(issue);
        };
    }
    getStacktrace() {
        const evt = this.props.event;
        const contentArr = (0, getStacktraceBody_1.default)(evt);
        if (contentArr && contentArr.length > 0) {
            return '\n\n```\n' + contentArr[0] + '\n```';
        }
        else {
            return '';
        }
    }
    getFieldDefault(field) {
        const { group, appName } = this.props;
        if (field.type === 'textarea') {
            field.maxRows = 10;
            field.autosize = true;
        }
        switch (field.default) {
            case 'issue.title':
                return group.title;
            case 'issue.description':
                const stacktrace = this.getStacktrace();
                const queryParams = { referrer: appName };
                const url = (0, queryString_1.addQueryParamsToExistingUrl)(group.permalink, queryParams);
                const shortId = group.shortId;
                return (0, locale_1.t)('Sentry Issue: [%s](%s)%s', shortId, url, stacktrace);
            default:
                return '';
        }
    }
    render() {
        return (<sentryAppExternalForm_1.default sentryAppInstallationUuid={this.props.sentryAppInstallation.uuid} appName={this.props.appName} config={this.props.config} action={this.props.action} element="issue-link" extraFields={{ groupId: this.props.group.id }} extraRequestBody={{ projectId: this.props.group.project.id }} onSubmitSuccess={this.onSubmitSuccess} 
        // Needs to bind to access this.props
        getFieldDefault={field => this.getFieldDefault(field)}/>);
    }
}
exports.SentryAppExternalIssueForm = SentryAppExternalIssueForm;
exports.default = SentryAppExternalIssueForm;
//# sourceMappingURL=sentryAppExternalIssueForm.jsx.map