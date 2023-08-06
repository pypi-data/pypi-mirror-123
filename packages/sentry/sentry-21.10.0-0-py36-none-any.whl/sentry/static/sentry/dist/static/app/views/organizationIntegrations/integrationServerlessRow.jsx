Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class IntegrationServerlessRow extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            submitting: false,
        };
        this.recordAction = (action) => {
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.serverless_function_action', {
                integration: this.props.integration.provider.key,
                integration_type: 'first_party',
                action,
                organization: this.props.organization,
            });
        };
        this.toggleEnable = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a, _b;
            const { serverlessFunction } = this.props;
            const action = this.enabled ? 'disable' : 'enable';
            const data = {
                action,
                target: serverlessFunction.name,
            };
            try {
                (0, indicator_1.addLoadingMessage)();
                this.setState({ submitting: true });
                // optimistically update enable state
                this.props.onUpdateFunction({ enabled: !this.enabled });
                this.recordAction(action);
                const resp = yield this.props.api.requestPromise(this.endpoint, {
                    method: 'POST',
                    data,
                });
                // update remaining after response
                this.props.onUpdateFunction(resp);
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Success'));
            }
            catch (err) {
                // restore original on failure
                this.props.onUpdateFunction(serverlessFunction);
                (0, indicator_1.addErrorMessage)((_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : (0, locale_1.t)('Error occurred'));
            }
            this.setState({ submitting: false });
        });
        this.updateVersion = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _c, _d;
            const { serverlessFunction } = this.props;
            const data = {
                action: 'updateVersion',
                target: serverlessFunction.name,
            };
            try {
                this.setState({ submitting: true });
                // don't know the latest version but at least optimistically remove the update button
                this.props.onUpdateFunction({ outOfDate: false });
                (0, indicator_1.addLoadingMessage)();
                this.recordAction('updateVersion');
                const resp = yield this.props.api.requestPromise(this.endpoint, {
                    method: 'POST',
                    data,
                });
                // update remaining after response
                this.props.onUpdateFunction(resp);
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Success'));
            }
            catch (err) {
                // restore original on failure
                this.props.onUpdateFunction(serverlessFunction);
                (0, indicator_1.addErrorMessage)((_d = (_c = err.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) !== null && _d !== void 0 ? _d : (0, locale_1.t)('Error occurred'));
            }
            this.setState({ submitting: false });
        });
    }
    get enabled() {
        return this.props.serverlessFunction.enabled;
    }
    get endpoint() {
        const orgSlug = this.props.organization.slug;
        return `/organizations/${orgSlug}/integrations/${this.props.integration.id}/serverless-functions/`;
    }
    renderLayerStatus() {
        const { serverlessFunction } = this.props;
        if (!serverlessFunction.outOfDate) {
            return this.enabled ? (0, locale_1.t)('Latest') : (0, locale_1.t)('Disabled');
        }
        return (<UpdateButton size="small" priority="primary" onClick={this.updateVersion}>
        {(0, locale_1.t)('Update')}
      </UpdateButton>);
    }
    render() {
        const { serverlessFunction } = this.props;
        const { version } = serverlessFunction;
        // during optimistic update, we might be enabled without a version
        const versionText = this.enabled && version > 0 ? <react_1.Fragment>&nbsp;|&nbsp;v{version}</react_1.Fragment> : null;
        return (<Item>
        <NameWrapper>
          <NameRuntimeVersionWrapper>
            <Name>{serverlessFunction.name}</Name>
            <RuntimeAndVersion>
              <DetailWrapper>{serverlessFunction.runtime}</DetailWrapper>
              <DetailWrapper>{versionText}</DetailWrapper>
            </RuntimeAndVersion>
          </NameRuntimeVersionWrapper>
        </NameWrapper>
        <LayerStatusWrapper>{this.renderLayerStatus()}</LayerStatusWrapper>
        <StyledSwitch isActive={this.enabled} isDisabled={this.state.submitting} size="sm" toggle={this.toggleEnable}/>
      </Item>);
    }
}
exports.default = (0, withApi_1.default)(IntegrationServerlessRow);
const Item = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};

  &:not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }

  display: grid;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;
  grid-template-columns: 2fr 1fr 0.5fr;
  grid-template-areas: 'function-name layer-status enable-switch';
`;
const ItemWrapper = (0, styled_1.default)('span') `
  height: 32px;
  vertical-align: middle;
  display: flex;
  align-items: center;
`;
const NameWrapper = (0, styled_1.default)(ItemWrapper) `
  grid-area: function-name;
`;
const LayerStatusWrapper = (0, styled_1.default)(ItemWrapper) `
  grid-area: layer-status;
`;
const StyledSwitch = (0, styled_1.default)(switchButton_1.default) `
  grid-area: enable-switch;
`;
const UpdateButton = (0, styled_1.default)(button_1.default) ``;
const NameRuntimeVersionWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
`;
const Name = (0, styled_1.default)(`span`) `
  padding-bottom: ${(0, space_1.default)(1)};
`;
const RuntimeAndVersion = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  color: ${p => p.theme.gray300};
`;
const DetailWrapper = (0, styled_1.default)('div') `
  line-height: 1.2;
`;
//# sourceMappingURL=integrationServerlessRow.jsx.map