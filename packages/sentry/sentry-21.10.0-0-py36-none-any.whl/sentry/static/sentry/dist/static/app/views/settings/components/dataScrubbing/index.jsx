Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const api_1 = require("app/api");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const add_1 = (0, tslib_1.__importDefault)(require("./modals/add"));
const edit_1 = (0, tslib_1.__importDefault)(require("./modals/edit"));
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
const convertRelayPiiConfig_1 = (0, tslib_1.__importDefault)(require("./convertRelayPiiConfig"));
const organizationRules_1 = (0, tslib_1.__importDefault)(require("./organizationRules"));
const submitRules_1 = (0, tslib_1.__importDefault)(require("./submitRules"));
const ADVANCED_DATASCRUBBING_LINK = 'https://docs.sentry.io/product/data-management-settings/scrubbing/advanced-datascrubbing/';
class DataScrubbing extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            rules: [],
            savedRules: [],
            relayPiiConfig: this.props.relayPiiConfig,
            orgRules: [],
        };
        this.api = new api_1.Client();
        this.handleOpenAddModal = () => {
            const { rules } = this.state;
            (0, modal_1.openModal)(modalProps => (<add_1.default {...modalProps} projectId={this.props.projectId} savedRules={rules} api={this.api} endpoint={this.props.endpoint} orgSlug={this.props.organization.slug} onSubmitSuccess={response => {
                    this.successfullySaved(response, (0, locale_1.t)('Successfully added data scrubbing rule'));
                }}/>));
        };
        this.handleOpenEditModal = (id) => () => {
            const { rules } = this.state;
            (0, modal_1.openModal)(modalProps => (<edit_1.default {...modalProps} rule={rules[id]} projectId={this.props.projectId} savedRules={rules} api={this.api} endpoint={this.props.endpoint} orgSlug={this.props.organization.slug} onSubmitSuccess={response => {
                    this.successfullySaved(response, (0, locale_1.t)('Successfully updated data scrubbing rule'));
                }}/>));
        };
        this.handleDelete = (id) => () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { rules } = this.state;
            const filteredRules = rules.filter(rule => rule.id !== id);
            try {
                const data = yield (0, submitRules_1.default)(this.api, this.props.endpoint, filteredRules);
                if (data === null || data === void 0 ? void 0 : data.relayPiiConfig) {
                    const convertedRules = (0, convertRelayPiiConfig_1.default)(data.relayPiiConfig);
                    this.setState({ rules: convertedRules });
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Successfully deleted data scrubbing rule'));
                }
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An unknown error occurred while deleting data scrubbing rule'));
            }
        });
    }
    componentDidMount() {
        this.loadRules();
        this.loadOrganizationRules();
    }
    componentDidUpdate(_prevProps, prevState) {
        if (prevState.relayPiiConfig !== this.state.relayPiiConfig) {
            this.loadRules();
        }
    }
    componentWillUnmount() {
        this.api.clear();
    }
    loadOrganizationRules() {
        const { organization, projectId } = this.props;
        if (projectId) {
            try {
                this.setState({
                    orgRules: (0, convertRelayPiiConfig_1.default)(organization.relayPiiConfig),
                });
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to load organization rules'));
            }
        }
    }
    loadRules() {
        try {
            const convertedRules = (0, convertRelayPiiConfig_1.default)(this.state.relayPiiConfig);
            this.setState({
                rules: convertedRules,
                savedRules: convertedRules,
            });
        }
        catch (_a) {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to load project rules'));
        }
    }
    successfullySaved(response, successMessage) {
        const { onSubmitSuccess } = this.props;
        this.setState({ rules: (0, convertRelayPiiConfig_1.default)(response.relayPiiConfig) });
        (0, indicator_1.addSuccessMessage)(successMessage);
        onSubmitSuccess === null || onSubmitSuccess === void 0 ? void 0 : onSubmitSuccess(response);
    }
    render() {
        const { additionalContext, disabled, projectId } = this.props;
        const { orgRules, rules } = this.state;
        return (<panels_1.Panel data-test-id="advanced-data-scrubbing" id="advanced-data-scrubbing">
        <panels_1.PanelHeader>
          <div>{(0, locale_1.t)('Advanced Data Scrubbing')}</div>
        </panels_1.PanelHeader>
        <panels_1.PanelAlert type="info">
          {additionalContext}{' '}
          {`${(0, locale_1.t)('The new rules will only apply to upcoming events. ')}`}{' '}
          {(0, locale_1.tct)('For more details, see [linkToDocs].', {
                linkToDocs: (<externalLink_1.default href={ADVANCED_DATASCRUBBING_LINK}>
                {(0, locale_1.t)('full documentation on data scrubbing')}
              </externalLink_1.default>),
            })}
        </panels_1.PanelAlert>
        <panels_1.PanelBody>
          {projectId && <organizationRules_1.default rules={orgRules}/>}
          <content_1.default rules={rules} onDeleteRule={this.handleDelete} onEditRule={this.handleOpenEditModal} disabled={disabled}/>
          <PanelAction>
            <button_1.default href={ADVANCED_DATASCRUBBING_LINK} target="_blank">
              {(0, locale_1.t)('Read the docs')}
            </button_1.default>
            <button_1.default disabled={disabled} onClick={this.handleOpenAddModal} priority="primary">
              {(0, locale_1.t)('Add Rule')}
            </button_1.default>
          </PanelAction>
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
exports.default = DataScrubbing;
const PanelAction = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  position: relative;
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-template-columns: auto auto;
  justify-content: flex-end;
  border-top: 1px solid ${p => p.theme.border};
`;
//# sourceMappingURL=index.jsx.map