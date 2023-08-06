Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const startCase_1 = (0, tslib_1.__importDefault)(require("lodash/startCase"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const pluginIcon_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/pluginIcon"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const marked_1 = (0, tslib_1.__importStar)(require("app/utils/marked"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const RequestIntegrationButton_1 = (0, tslib_1.__importDefault)(require("./integrationRequest/RequestIntegrationButton"));
const integrationStatus_1 = (0, tslib_1.__importDefault)(require("./integrationStatus"));
class AbstractIntegrationDetailedView extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.tabs = ['overview', 'configurations'];
        this.onTabChange = (value) => {
            this.trackIntegrationAnalytics('integrations.integration_tab_clicked', {
                integration_tab: value,
            });
            this.setState({ tab: value });
        };
        // Wrapper around trackIntegrationAnalytics that automatically provides many fields and the org
        this.trackIntegrationAnalytics = (eventKey, options) => {
            options = options || {};
            // If we use this intermediate type we get type checking on the things we care about
            const params = Object.assign({ view: 'integrations_directory_integration_detail', integration: this.integrationSlug, integration_type: this.integrationType, already_installed: this.installationStatus !== 'Not Installed', organization: this.props.organization }, options);
            (0, integrationUtil_1.trackIntegrationAnalytics)(eventKey, params);
        };
    }
    componentDidMount() {
        const { location } = this.props;
        const value = location.query.tab === 'configurations' ? 'configurations' : 'overview';
        // eslint-disable-next-line react/no-did-mount-set-state
        this.setState({ tab: value });
    }
    onLoadAllEndpointsSuccess() {
        this.trackIntegrationAnalytics('integrations.integration_viewed', {
            integration_tab: this.state.tab,
        });
    }
    /**
     * Abstract methods defined below
     */
    // The analytics type used in analytics which is snake case
    get integrationType() {
        // Allow children to implement this
        throw new Error('Not implemented');
    }
    get description() {
        // Allow children to implement this
        throw new Error('Not implemented');
    }
    get author() {
        // Allow children to implement this
        throw new Error('Not implemented');
    }
    get alerts() {
        // default is no alerts
        return [];
    }
    // Returns a list of the resources displayed at the bottom of the overview card
    get resourceLinks() {
        // Allow children to implement this
        throw new Error('Not implemented');
    }
    get installationStatus() {
        // Allow children to implement this
        throw new Error('Not implemented');
    }
    get integrationName() {
        // Allow children to implement this
        throw new Error('Not implemented');
    }
    // Returns an array of RawIntegrationFeatures which is used in feature gating
    // and displaying what the integration does
    get featureData() {
        // Allow children to implement this
        throw new Error('Not implemented');
    }
    getIcon(title) {
        switch (title) {
            case 'View Source':
                return <icons_1.IconProject />;
            case 'Report Issue':
                return <icons_1.IconGithub />;
            case 'Documentation':
            case 'Splunk Setup Instructions':
            case 'Trello Setup Instructions':
                return <icons_1.IconDocs />;
            default:
                return <icons_1.IconGeneric />;
        }
    }
    // Returns the string that is shown as the title of a tab
    getTabDisplay(tab) {
        // default is return the tab
        return tab;
    }
    // Render the button at the top which is usually just an installation button
    renderTopButton(_disabledFromFeatures, // from the feature gate
    _userHasAccess // from user permissions
    ) {
        // Allow children to implement this
        throw new Error('Not implemented');
    }
    // Returns the permission descriptions, only use by Sentry Apps
    renderPermissions() {
        // default is don't render permissions
        return null;
    }
    renderEmptyConfigurations() {
        return (<panels_1.Panel>
        <emptyMessage_1.default title={(0, locale_1.t)("You haven't set anything up yet")} description={(0, locale_1.t)('But that doesn’t have to be the case for long! Add an installation to get started.')} action={this.renderAddInstallButton(true)}/>
      </panels_1.Panel>);
    }
    // Returns the list of configurations for the integration
    renderConfigurations() {
        // Allow children to implement this
        throw new Error('Not implemented');
    }
    /**
     * Actually implemented methods below
     */
    get integrationSlug() {
        return this.props.params.integrationSlug;
    }
    // Returns the props as needed by the hooks integrations:feature-gates
    get featureProps() {
        const { organization } = this.props;
        const featureData = this.featureData;
        // Prepare the features list
        const features = featureData.map(f => ({
            featureGate: f.featureGate,
            description: (<FeatureListItem dangerouslySetInnerHTML={{ __html: (0, marked_1.singleLineRenderer)(f.description) }}/>),
        }));
        return { organization, features };
    }
    cleanTags() {
        return (0, integrationUtil_1.getCategories)(this.featureData);
    }
    renderRequestIntegrationButton() {
        return (<RequestIntegrationButton_1.default organization={this.props.organization} name={this.integrationName} slug={this.integrationSlug} type={this.integrationType}/>);
    }
    renderAddInstallButton(hideButtonIfDisabled = false) {
        const { organization } = this.props;
        const { IntegrationDirectoryFeatures } = (0, integrationUtil_1.getIntegrationFeatureGate)();
        return (<IntegrationDirectoryFeatures {...this.featureProps}>
        {({ disabled, disabledReason }) => (<DisableWrapper>
            <access_1.default organization={organization} access={['org:integrations']}>
              {({ hasAccess }) => (<tooltip_1.default title={(0, locale_1.t)('You must be an organization owner, manager or admin to install this.')} disabled={hasAccess}>
                  {!hideButtonIfDisabled && disabled ? (<div />) : (this.renderTopButton(disabled, hasAccess))}
                </tooltip_1.default>)}
            </access_1.default>
            {disabled && <DisabledNotice reason={disabledReason}/>}
          </DisableWrapper>)}
      </IntegrationDirectoryFeatures>);
    }
    // Returns the content shown in the top section of the integration detail
    renderTopSection() {
        const tags = this.cleanTags();
        return (<Flex>
        <pluginIcon_1.default pluginId={this.integrationSlug} size={50}/>
        <NameContainer>
          <Flex>
            <Name>{this.integrationName}</Name>
            <StatusWrapper>
              {this.installationStatus && (<integrationStatus_1.default status={this.installationStatus}/>)}
            </StatusWrapper>
          </Flex>
          <Flex>
            {tags.map(feature => (<StyledTag key={feature}>{(0, startCase_1.default)(feature)}</StyledTag>))}
          </Flex>
        </NameContainer>
        {this.renderAddInstallButton()}
      </Flex>);
    }
    // Returns the tabs divider with the clickable tabs
    renderTabs() {
        // TODO: Convert to styled component
        return (<ul className="nav nav-tabs border-bottom" style={{ paddingTop: '30px' }}>
        {this.tabs.map(tabName => (<li key={tabName} className={this.state.tab === tabName ? 'active' : ''} onClick={() => this.onTabChange(tabName)}>
            <CapitalizedLink>{(0, locale_1.t)(this.getTabDisplay(tabName))}</CapitalizedLink>
          </li>))}
      </ul>);
    }
    // Returns the information about the integration description and features
    renderInformationCard() {
        const { IntegrationDirectoryFeatureList } = (0, integrationUtil_1.getIntegrationFeatureGate)();
        return (<React.Fragment>
        <Flex>
          <FlexContainer>
            <Description dangerouslySetInnerHTML={{ __html: (0, marked_1.default)(this.description) }}/>
            <IntegrationDirectoryFeatureList {...this.featureProps} provider={{ key: this.props.params.integrationSlug }}/>
            {this.renderPermissions()}
            {this.alerts.map((alert, i) => (<alert_1.default key={i} type={alert.type} icon={alert.icon}>
                <span dangerouslySetInnerHTML={{ __html: (0, marked_1.singleLineRenderer)(alert.text) }}/>
              </alert_1.default>))}
          </FlexContainer>
          <Metadata>
            {!!this.author && (<AuthorInfo>
                <CreatedContainer>{(0, locale_1.t)('Created By')}</CreatedContainer>
                <div>{this.author}</div>
              </AuthorInfo>)}
            {this.resourceLinks.map(({ title, url }) => (<ExternalLinkContainer key={url}>
                {this.getIcon(title)}
                <externalLink_1.default href={url}>{(0, locale_1.t)(title)}</externalLink_1.default>
              </ExternalLinkContainer>))}
          </Metadata>
        </Flex>
      </React.Fragment>);
    }
    renderBody() {
        return (<React.Fragment>
        {this.renderTopSection()}
        {this.renderTabs()}
        {this.state.tab === 'overview'
                ? this.renderInformationCard()
                : this.renderConfigurations()}
      </React.Fragment>);
    }
}
const Flex = (0, styled_1.default)('div') `
  display: flex;
`;
const FlexContainer = (0, styled_1.default)('div') `
  flex: 1;
`;
const CapitalizedLink = (0, styled_1.default)('a') `
  text-transform: capitalize;
`;
const StyledTag = (0, styled_1.default)(tag_1.default) `
  text-transform: none;
  &:not(:first-child) {
    margin-left: ${(0, space_1.default)(0.5)};
  }
`;
const NameContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  justify-content: center;
  padding-left: ${(0, space_1.default)(2)};
`;
const Name = (0, styled_1.default)('div') `
  font-weight: bold;
  font-size: 1.4em;
  margin-bottom: ${(0, space_1.default)(1)};
`;
const IconCloseCircle = (0, styled_1.default)(icons_1.IconClose) `
  color: ${p => p.theme.red300};
  margin-right: ${(0, space_1.default)(1)};
`;
const DisabledNotice = (0, styled_1.default)((_a) => {
    var { reason } = _a, p = (0, tslib_1.__rest)(_a, ["reason"]);
    return (<div style={{
            display: 'flex',
            alignItems: 'center',
        }} {...p}>
    <IconCloseCircle isCircled/>
    <span>{reason}</span>
  </div>);
}) `
  padding-top: ${(0, space_1.default)(0.5)};
  font-size: 0.9em;
`;
const FeatureListItem = (0, styled_1.default)('span') `
  line-height: 24px;
`;
const Description = (0, styled_1.default)('div') `
  font-size: 1.5rem;
  line-height: 2.1rem;
  margin-bottom: ${(0, space_1.default)(2)};

  li {
    margin-bottom: 6px;
  }
`;
const Metadata = (0, styled_1.default)(Flex) `
  display: grid;
  grid-auto-rows: max-content;
  grid-auto-flow: row;
  grid-gap: ${(0, space_1.default)(2)};
  font-size: 0.9em;
  margin-left: ${(0, space_1.default)(4)};
  margin-right: 100px;
`;
const AuthorInfo = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(3)};
`;
const ExternalLinkContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
`;
const StatusWrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(1)};
  padding-left: ${(0, space_1.default)(2)};
  line-height: 1.5em;
`;
const DisableWrapper = (0, styled_1.default)('div') `
  margin-left: auto;
  align-self: center;
  display: flex;
  flex-direction: column;
  align-items: center;
`;
const CreatedContainer = (0, styled_1.default)('div') `
  text-transform: uppercase;
  padding-bottom: ${(0, space_1.default)(1)};
  color: ${p => p.theme.gray300};
  font-weight: 600;
  font-size: 12px;
`;
exports.default = AbstractIntegrationDetailedView;
//# sourceMappingURL=abstractIntegrationDetailedView.jsx.map