Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const indicator_1 = require("app/actionCreators/indicator");
const abstractExternalIssueForm_1 = (0, tslib_1.__importDefault)(require("app/components/externalIssues/abstractExternalIssueForm"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const locale_1 = require("app/locale");
const MESSAGES_BY_ACTION = {
    link: (0, locale_1.t)('Successfully linked issue.'),
    create: (0, locale_1.t)('Successfully created issue.'),
};
const SUBMIT_LABEL_BY_ACTION = {
    link: (0, locale_1.t)('Link Issue'),
    create: (0, locale_1.t)('Create Issue'),
};
class ExternalIssueForm extends abstractExternalIssueForm_1.default {
    constructor(props) {
        super(props, {});
        this.handleClick = (action) => {
            this.setState({ action }, () => this.reloadData());
        };
        this.startTransaction = (type) => {
            const { group, integration } = this.props;
            const { action } = this.state;
            const transaction = Sentry.startTransaction({ name: `externalIssueForm.${type}` });
            Sentry.getCurrentHub().configureScope(scope => scope.setSpan(transaction));
            transaction.setTag('issueAction', action);
            transaction.setTag('groupID', group.id);
            transaction.setTag('projectID', group.project.id);
            transaction.setTag('integrationSlug', integration.provider.slug);
            transaction.setTag('integrationType', 'firstParty');
            return transaction;
        };
        this.handlePreSubmit = () => {
            this.submitTransaction = this.startTransaction('submit');
        };
        this.onSubmitSuccess = (_data) => {
            var _a;
            const { onChange, closeModal } = this.props;
            const { action } = this.state;
            onChange(() => (0, indicator_1.addSuccessMessage)(MESSAGES_BY_ACTION[action]));
            closeModal();
            (_a = this.submitTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        this.handleSubmitError = () => {
            var _a;
            (_a = this.submitTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        this.onLoadAllEndpointsSuccess = () => {
            var _a;
            (_a = this.loadTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        this.onRequestError = () => {
            var _a;
            (_a = this.loadTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        this.getTitle = () => {
            const { integration } = this.props;
            return (0, locale_1.tct)('[integration] Issue', { integration: integration.provider.name });
        };
        this.getFormProps = () => {
            const { action } = this.state;
            return Object.assign(Object.assign({}, this.getDefaultFormProps()), { submitLabel: SUBMIT_LABEL_BY_ACTION[action], apiEndpoint: this.getEndPointString(), apiMethod: action === 'create' ? 'POST' : 'PUT', onPreSubmit: this.handlePreSubmit, onSubmitError: this.handleSubmitError, onSubmitSuccess: this.onSubmitSuccess });
        };
        this.renderNavTabs = () => {
            const { action } = this.state;
            return (<navTabs_1.default underlined>
        <li className={action === 'create' ? 'active' : ''}>
          <a onClick={() => this.handleClick('create')}>{(0, locale_1.t)('Create')}</a>
        </li>
        <li className={action === 'link' ? 'active' : ''}>
          <a onClick={() => this.handleClick('link')}>{(0, locale_1.t)('Link')}</a>
        </li>
      </navTabs_1.default>);
        };
        this.loadTransaction = this.startTransaction('load');
    }
    getEndpoints() {
        var _a;
        const query = {};
        if ((_a = this.state) === null || _a === void 0 ? void 0 : _a.hasOwnProperty('action')) {
            query.action = this.state.action;
        }
        return [['integrationDetails', this.getEndPointString(), { query }]];
    }
    getEndPointString() {
        const { group, integration } = this.props;
        return `/groups/${group.id}/integrations/${integration.id}/`;
    }
    renderBody() {
        return this.renderForm(this.getCleanedFields());
    }
}
exports.default = ExternalIssueForm;
//# sourceMappingURL=externalIssueForm.jsx.map