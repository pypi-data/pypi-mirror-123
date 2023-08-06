Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const sentryAppPublishRequestModal_1 = (0, tslib_1.__importDefault)(require("app/components/modals/sentryAppPublishRequestModal"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const pluginIcon_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/pluginIcon"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const sentryApplicationRowButtons_1 = (0, tslib_1.__importDefault)(require("./sentryApplicationRowButtons"));
class SentryApplicationRow extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.handlePublish = () => {
            const { app } = this.props;
            (0, modal_1.openModal)(deps => <sentryAppPublishRequestModal_1.default app={app} {...deps}/>);
        };
    }
    get isInternal() {
        return this.props.app.status === 'internal';
    }
    hideStatus() {
        // no publishing for internal apps so hide the status on the developer settings page
        return this.isInternal;
    }
    renderStatus() {
        const { app } = this.props;
        if (this.hideStatus()) {
            return null;
        }
        return <PublishStatus status={app.status}/>;
    }
    render() {
        const { app, organization, onRemoveApp } = this.props;
        return (<SentryAppItem data-test-id={app.slug}>
        <StyledFlex>
          <pluginIcon_1.default size={36} pluginId={app.slug}/>
          <SentryAppBox>
            <SentryAppName hideStatus={this.hideStatus()}>
              <link_1.default to={`/settings/${organization.slug}/developer-settings/${app.slug}/`}>
                {app.name}
              </link_1.default>
            </SentryAppName>
            <SentryAppDetails>{this.renderStatus()}</SentryAppDetails>
          </SentryAppBox>

          <Box>
            <sentryApplicationRowButtons_1.default organization={organization} app={app} onClickRemove={onRemoveApp} onClickPublish={this.handlePublish}/>
          </Box>
        </StyledFlex>
      </SentryAppItem>);
    }
}
exports.default = SentryApplicationRow;
const Flex = (0, styled_1.default)('div') `
  display: flex;
`;
const Box = (0, styled_1.default)('div') ``;
const SentryAppItem = (0, styled_1.default)(panels_1.PanelItem) `
  flex-direction: column;
  padding: 5px;
`;
const StyledFlex = (0, styled_1.default)(Flex) `
  justify-content: center;
  padding: 10px;
`;
const SentryAppBox = (0, styled_1.default)('div') `
  padding-left: 15px;
  padding-right: 15px;
  flex: 1;
`;
const SentryAppDetails = (0, styled_1.default)(Flex) `
  align-items: center;
  margin-top: 6px;
  font-size: 0.8em;
`;
const SentryAppName = (0, styled_1.default)('div') `
  margin-top: ${p => (p.hideStatus ? '10px' : '0px')};
`;
const CenterFlex = (0, styled_1.default)(Flex) `
  align-items: center;
`;
const PublishStatus = (0, styled_1.default)((_a) => {
    var { status } = _a, props = (0, tslib_1.__rest)(_a, ["status"]);
    return (<CenterFlex>
    <div {...props}>{(0, locale_1.t)(`${status}`)}</div>
  </CenterFlex>);
}) `
  color: ${(props) => props.status === 'published' ? props.theme.success : props.theme.gray300};
  font-weight: light;
  margin-right: ${(0, space_1.default)(0.75)};
`;
//# sourceMappingURL=index.jsx.map