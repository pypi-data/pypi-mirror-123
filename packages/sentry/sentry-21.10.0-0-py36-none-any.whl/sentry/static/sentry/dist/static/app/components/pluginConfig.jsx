Object.defineProperty(exports, "__esModule", { value: true });
exports.PluginConfig = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const plugins_1 = (0, tslib_1.__importDefault)(require("app/plugins"));
const pluginIcon_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/pluginIcon"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class PluginConfig extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: !plugins_1.default.isLoaded(this.props.data),
            testResults: '',
        };
        this.handleDisablePlugin = () => {
            this.props.onDisablePlugin(this.props.data);
        };
        this.handleTestPlugin = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({ testResults: '' });
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Sending test...'));
            try {
                const data = yield this.props.api.requestPromise(this.getPluginEndpoint(), {
                    method: 'POST',
                    data: {
                        test: true,
                    },
                });
                this.setState({ testResults: JSON.stringify(data.detail) });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Test Complete!'));
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An unexpected error occurred while testing your plugin. Please try again.'));
            }
        });
    }
    componentDidMount() {
        this.loadPlugin(this.props.data);
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        this.loadPlugin(nextProps.data);
    }
    shouldComponentUpdate(nextProps, nextState) {
        return !(0, isEqual_1.default)(nextState, this.state) || !(0, isEqual_1.default)(nextProps.data, this.props.data);
    }
    loadPlugin(data) {
        this.setState({
            loading: true,
        }, () => {
            plugins_1.default.load(data, () => {
                this.setState({ loading: false });
            });
        });
    }
    getPluginEndpoint() {
        const { organization, project, data } = this.props;
        return `/projects/${organization.slug}/${project.slug}/plugins/${data.id}/`;
    }
    createMarkup() {
        return { __html: this.props.data.doc };
    }
    render() {
        const { data } = this.props;
        // If passed via props, use that value instead of from `data`
        const enabled = typeof this.props.enabled !== 'undefined' ? this.props.enabled : data.enabled;
        return (<panels_1.Panel className={`plugin-config ref-plugin-config-${data.id}`} data-test-id="plugin-config">
        <panels_1.PanelHeader hasButtons>
          <PluginName>
            <StyledPluginIcon pluginId={data.id}/>
            <span>{data.name}</span>
          </PluginName>

          {data.canDisable && enabled && (<Actions>
              {data.isTestable && (<TestPluginButton onClick={this.handleTestPlugin} size="small">
                  {(0, locale_1.t)('Test Plugin')}
                </TestPluginButton>)}
              <button_1.default size="small" onClick={this.handleDisablePlugin}>
                {(0, locale_1.t)('Disable')}
              </button_1.default>
            </Actions>)}
        </panels_1.PanelHeader>

        {data.status === 'beta' && (<panels_1.PanelAlert type="warning">
            {(0, locale_1.t)('This plugin is considered beta and may change in the future.')}
          </panels_1.PanelAlert>)}

        {this.state.testResults !== '' && (<panels_1.PanelAlert type="info">
            <strong>Test Results</strong>
            <div>{this.state.testResults}</div>
          </panels_1.PanelAlert>)}

        <StyledPanelBody>
          <div dangerouslySetInnerHTML={this.createMarkup()}/>
          {this.state.loading ? (<loadingIndicator_1.default />) : (plugins_1.default.get(data).renderSettings({
                organization: this.props.organization,
                project: this.props.project,
            }))}
        </StyledPanelBody>
      </panels_1.Panel>);
    }
}
exports.PluginConfig = PluginConfig;
PluginConfig.defaultProps = {
    onDisablePlugin: () => { },
};
exports.default = (0, withApi_1.default)(PluginConfig);
const PluginName = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  flex: 1;
`;
const StyledPluginIcon = (0, styled_1.default)(pluginIcon_1.default) `
  margin-right: ${(0, space_1.default)(1)};
`;
const Actions = (0, styled_1.default)('div') `
  display: flex;
`;
const TestPluginButton = (0, styled_1.default)(button_1.default) `
  margin-right: ${(0, space_1.default)(1)};
`;
const StyledPanelBody = (0, styled_1.default)(panels_1.PanelBody) `
  padding: ${(0, space_1.default)(2)};
  padding-bottom: 0;
`;
//# sourceMappingURL=pluginConfig.jsx.map