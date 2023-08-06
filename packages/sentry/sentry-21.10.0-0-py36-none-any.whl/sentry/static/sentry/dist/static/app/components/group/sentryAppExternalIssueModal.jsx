Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const sentryAppExternalIssueForm_1 = (0, tslib_1.__importDefault)(require("app/components/group/sentryAppExternalIssueForm"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class SentryAppExternalIssueModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            action: 'create',
        };
        this.showLink = () => {
            this.setState({ action: 'link' });
        };
        this.showCreate = () => {
            this.setState({ action: 'create' });
        };
        this.onSubmitSuccess = (externalIssue) => {
            this.props.onSubmitSuccess(externalIssue);
            this.props.closeModal();
        };
    }
    render() {
        const { Header, Body, sentryAppComponent, sentryAppInstallation, group } = this.props;
        const { action } = this.state;
        const name = sentryAppComponent.sentryApp.name;
        const config = sentryAppComponent.schema[action];
        return (<react_1.Fragment>
        <Header closeButton>{(0, locale_1.tct)('[name] Issue', { name })}</Header>
        <navTabs_1.default underlined>
          <li className={action === 'create' ? 'active create' : 'create'}>
            <a onClick={this.showCreate}>{(0, locale_1.t)('Create')}</a>
          </li>
          <li className={action === 'link' ? 'active link' : 'link'}>
            <a onClick={this.showLink}>{(0, locale_1.t)('Link')}</a>
          </li>
        </navTabs_1.default>
        <Body>
          <sentryAppExternalIssueForm_1.default group={group} sentryAppInstallation={sentryAppInstallation} appName={name} config={config} action={action} onSubmitSuccess={this.onSubmitSuccess} event={this.props.event}/>
        </Body>
      </react_1.Fragment>);
    }
}
exports.default = (0, withApi_1.default)(SentryAppExternalIssueModal);
//# sourceMappingURL=sentryAppExternalIssueModal.jsx.map