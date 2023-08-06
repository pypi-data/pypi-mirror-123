Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const organizations_1 = require("app/actionCreators/organizations");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organization/permissionAlert"));
const add_1 = (0, tslib_1.__importDefault)(require("./modals/add"));
const edit_1 = (0, tslib_1.__importDefault)(require("./modals/edit"));
const emptyState_1 = (0, tslib_1.__importDefault)(require("./emptyState"));
const list_1 = (0, tslib_1.__importDefault)(require("./list"));
const RELAY_DOCS_LINK = 'https://getsentry.github.io/relay/';
class RelayWrapper extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleDelete = (publicKey) => () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { relays } = this.state;
            const trustedRelays = relays
                .filter(relay => relay.publicKey !== publicKey)
                .map(relay => (0, omit_1.default)(relay, ['created', 'lastModified']));
            try {
                const response = yield this.api.requestPromise(`/organizations/${this.props.organization.slug}/`, {
                    method: 'PUT',
                    data: { trustedRelays },
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Successfully deleted Relay public key'));
                this.setRelays(response.trustedRelays);
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An unknown error occurred while deleting Relay public key'));
            }
        });
        this.handleOpenEditDialog = (publicKey) => () => {
            const editRelay = this.state.relays.find(relay => relay.publicKey === publicKey);
            if (!editRelay) {
                return;
            }
            (0, modal_1.openModal)(modalProps => (<edit_1.default {...modalProps} savedRelays={this.state.relays} api={this.api} orgSlug={this.props.organization.slug} relay={editRelay} onSubmitSuccess={response => {
                    this.successfullySaved(response, (0, locale_1.t)('Successfully updated Relay public key'));
                }}/>));
        };
        this.handleOpenAddDialog = () => {
            (0, modal_1.openModal)(modalProps => (<add_1.default {...modalProps} savedRelays={this.state.relays} api={this.api} orgSlug={this.props.organization.slug} onSubmitSuccess={response => {
                    this.successfullySaved(response, (0, locale_1.t)('Successfully added Relay public key'));
                }}/>));
        };
        this.handleRefresh = () => {
            // Fetch fresh activities
            this.fetchData();
        };
    }
    componentDidUpdate(prevProps, prevState) {
        if (!(0, isEqual_1.default)(prevState.relays, this.state.relays)) {
            // Fetch fresh activities
            this.fetchData();
            (0, organizations_1.updateOrganization)(Object.assign(Object.assign({}, prevProps.organization), { trustedRelays: this.state.relays }));
        }
        super.componentDidUpdate(prevProps, prevState);
    }
    getTitle() {
        return (0, locale_1.t)('Relay');
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { relays: this.props.organization.trustedRelays });
    }
    getEndpoints() {
        const { organization } = this.props;
        return [['relayActivities', `/organizations/${organization.slug}/relay_usage/`]];
    }
    setRelays(trustedRelays) {
        this.setState({ relays: trustedRelays });
    }
    successfullySaved(response, successMessage) {
        (0, indicator_1.addSuccessMessage)(successMessage);
        this.setRelays(response.trustedRelays);
    }
    renderContent(disabled) {
        const { relays, relayActivities, loading } = this.state;
        if (loading) {
            return this.renderLoading();
        }
        if (!relays.length) {
            return <emptyState_1.default />;
        }
        return (<list_1.default relays={relays} relayActivities={relayActivities} onEdit={this.handleOpenEditDialog} onRefresh={this.handleRefresh} onDelete={this.handleDelete} disabled={disabled}/>);
    }
    renderBody() {
        const { organization } = this.props;
        const disabled = !organization.access.includes('org:write');
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Relay')} action={<button_1.default title={disabled ? (0, locale_1.t)('You do not have permission to register keys') : undefined} priority="primary" size="small" icon={<icons_1.IconAdd size="xs" isCircled/>} onClick={this.handleOpenAddDialog} disabled={disabled}>
              {(0, locale_1.t)('Register Key')}
            </button_1.default>}/>
        <permissionAlert_1.default />
        <textBlock_1.default>
          {(0, locale_1.tct)('Sentry Relay offers enterprise-grade data security by providing a standalone service that acts as a middle layer between your application and sentry.io. Go to [link:Relay Documentation] for setup and details.', { link: <externalLink_1.default href={RELAY_DOCS_LINK}/> })}
        </textBlock_1.default>
        {this.renderContent(disabled)}
      </react_1.Fragment>);
    }
}
exports.default = RelayWrapper;
//# sourceMappingURL=relayWrapper.jsx.map