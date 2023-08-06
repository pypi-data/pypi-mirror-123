Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const startCase_1 = (0, tslib_1.__importDefault)(require("lodash/startCase"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const pluginIcon_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/pluginIcon"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const integrationStatus_1 = (0, tslib_1.__importDefault)(require("./integrationStatus"));
const pluginDeprecationAlert_1 = (0, tslib_1.__importDefault)(require("./pluginDeprecationAlert"));
const urlMap = {
    plugin: 'plugins',
    firstParty: 'integrations',
    sentryApp: 'sentry-apps',
    documentIntegration: 'document-integrations',
};
const IntegrationRow = (props) => {
    const { organization, type, slug, displayName, status, publishStatus, configurations, categories, alertText, resolveText, plugin, } = props;
    const baseUrl = publishStatus === 'internal'
        ? `/settings/${organization.slug}/developer-settings/${slug}/`
        : `/settings/${organization.slug}/${urlMap[type]}/${slug}/`;
    const renderDetails = () => {
        if (type === 'sentryApp') {
            return publishStatus !== 'published' && <PublishStatus status={publishStatus}/>;
        }
        // TODO: Use proper translations
        return configurations > 0 ? (<StyledLink to={`${baseUrl}?tab=configurations`}>{`${configurations} Configuration${configurations > 1 ? 's' : ''}`}</StyledLink>) : null;
    };
    const renderStatus = () => {
        // status should be undefined for document integrations
        if (status) {
            return <integrationStatus_1.default status={status}/>;
        }
        return <LearnMore to={baseUrl}>{(0, locale_1.t)('Learn More')}</LearnMore>;
    };
    return (<PanelRow noPadding data-test-id={slug}>
      <FlexContainer>
        <pluginIcon_1.default size={36} pluginId={slug}/>
        <Container>
          <IntegrationName to={baseUrl}>{displayName}</IntegrationName>
          <IntegrationDetails>
            {renderStatus()}
            {renderDetails()}
          </IntegrationDetails>
        </Container>
        <InternalContainer>
          {categories === null || categories === void 0 ? void 0 : categories.map(category => (<CategoryTag key={category} category={(0, startCase_1.default)(category)} priority={category === publishStatus}/>))}
        </InternalContainer>
      </FlexContainer>
      {alertText && (<AlertContainer>
          <alert_1.default type="warning" icon={<icons_1.IconWarning size="sm"/>}>
            <span>{alertText}</span>
            <ResolveNowButton href={`${baseUrl}?tab=configurations&referrer=directory_resolve_now`} size="xsmall" onClick={() => (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.resolve_now_clicked', {
                integration_type: (0, integrationUtil_1.convertIntegrationTypeToSnakeCase)(type),
                integration: slug,
                organization,
            })}>
              {resolveText || (0, locale_1.t)('Resolve Now')}
            </ResolveNowButton>
          </alert_1.default>
        </AlertContainer>)}
      {(plugin === null || plugin === void 0 ? void 0 : plugin.deprecationDate) && (<PluginDeprecationAlertWrapper>
          <pluginDeprecationAlert_1.default organization={organization} plugin={plugin}/>
        </PluginDeprecationAlertWrapper>)}
    </PanelRow>);
};
const PluginDeprecationAlertWrapper = (0, styled_1.default)('div') `
  padding: 0px ${(0, space_1.default)(3)} 0px 68px;
`;
const PanelRow = (0, styled_1.default)(panels_1.PanelItem) `
  flex-direction: column;
`;
const FlexContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(2)};
`;
const InternalContainer = (0, styled_1.default)(FlexContainer) `
  padding: 0 ${(0, space_1.default)(2)};
`;
const Container = (0, styled_1.default)('div') `
  flex: 1;
  padding: 0 16px;
`;
const IntegrationName = (0, styled_1.default)(link_1.default) `
  font-weight: bold;
`;
const IntegrationDetails = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-top: 6px;
  font-size: 0.8em;
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.gray300};
  &:before {
    content: '|';
    color: ${p => p.theme.gray200};
    margin-right: ${(0, space_1.default)(0.75)};
    font-weight: normal;
  }
`;
const LearnMore = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.gray300};
`;
const PublishStatus = (0, styled_1.default)((_a) => {
    var { status } = _a, props = (0, tslib_1.__rest)(_a, ["status"]);
    return (<div {...props}>{(0, locale_1.t)(`${status}`)}</div>);
}) `
  color: ${(props) => props.status === 'published' ? props.theme.success : props.theme.gray300};
  font-weight: light;
  margin-right: ${(0, space_1.default)(0.75)};
  text-transform: capitalize;
  &:before {
    content: '|';
    color: ${p => p.theme.gray200};
    margin-right: ${(0, space_1.default)(0.75)};
    font-weight: normal;
  }
`;
// TODO(Priscila): Replace this component with the Tag component
const CategoryTag = (0, styled_1.default)((_a) => {
    var { priority: _priority, category } = _a, p = (0, tslib_1.__rest)(_a, ["priority", "category"]);
    return <div {...p}>{category}</div>;
}) `
  display: flex;
  flex-direction: row;
  padding: 1px 10px;
  background: ${p => (p.priority ? p.theme.purple200 : p.theme.gray100)};
  border-radius: 20px;
  font-size: ${(0, space_1.default)(1.5)};
  margin-right: ${(0, space_1.default)(1)};
  line-height: ${(0, space_1.default)(3)};
  text-align: center;
  color: ${p => (p.priority ? p.theme.white : p.theme.gray500)};
`;
const ResolveNowButton = (0, styled_1.default)(button_1.default) `
  color: ${p => p.theme.subText};
  float: right;
`;
const AlertContainer = (0, styled_1.default)('div') `
  padding: 0px ${(0, space_1.default)(3)} 0px 68px;
`;
exports.default = IntegrationRow;
//# sourceMappingURL=integrationRow.jsx.map