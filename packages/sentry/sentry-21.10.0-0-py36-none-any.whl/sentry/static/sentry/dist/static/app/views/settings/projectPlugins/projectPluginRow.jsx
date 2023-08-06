Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const locale_1 = require("app/locale");
const pluginIcon_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/pluginIcon"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const grayText = (0, react_2.css) `
  color: #979ba0;
`;
class ProjectPluginRow extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.handleChange = () => {
            const { onChange, id, enabled } = this.props;
            onChange(id, !enabled);
            const eventKey = !enabled ? 'integrations.enabled' : 'integrations.disabled';
            (0, integrationUtil_1.trackIntegrationAnalytics)(eventKey, {
                integration: id,
                integration_type: 'plugin',
                view: 'legacy_integrations',
                organization: this.props.organization,
            });
        };
    }
    render() {
        const { id, name, slug, version, author, hasConfiguration, enabled, canDisable } = this.props;
        const configureUrl = (0, recreateRoute_1.default)(id, this.props);
        return (<access_1.default access={['project:write']}>
        {({ hasAccess }) => {
                const LinkOrSpan = hasAccess ? link_1.default : 'span';
                return (<PluginItem key={id} className={slug}>
              <PluginInfo>
                <StyledPluginIcon size={48} pluginId={id}/>
                <PluginDescription>
                  <PluginName>
                    {`${name} `}
                    {(0, getDynamicText_1.default)({
                        value: (<Version>{version ? `v${version}` : <em>{(0, locale_1.t)('n/a')}</em>}</Version>),
                        fixed: <Version>v10</Version>,
                    })}
                  </PluginName>
                  <div>
                    {author && (<externalLink_1.default css={grayText} href={author.url}>
                        {author.name}
                      </externalLink_1.default>)}
                    {hasConfiguration && (<span>
                        {' '}
                        &middot;{' '}
                        <LinkOrSpan css={grayText} to={configureUrl}>
                          {(0, locale_1.t)('Configure plugin')}
                        </LinkOrSpan>
                      </span>)}
                  </div>
                </PluginDescription>
              </PluginInfo>
              <switchButton_1.default size="lg" isDisabled={!hasAccess || !canDisable} isActive={enabled} toggle={this.handleChange}/>
            </PluginItem>);
            }}
      </access_1.default>);
    }
}
exports.default = (0, withOrganization_1.default)(ProjectPluginRow);
const PluginItem = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  align-items: center;
`;
const PluginDescription = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  flex-direction: column;
`;
const PluginInfo = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  line-height: 24px;
`;
const PluginName = (0, styled_1.default)('div') `
  font-size: 16px;
`;
const StyledPluginIcon = (0, styled_1.default)(pluginIcon_1.default) `
  margin-right: 16px;
`;
// Keeping these colors the same from old integrations page
const Version = (0, styled_1.default)('span') `
  color: #babec2;
`;
//# sourceMappingURL=projectPluginRow.jsx.map