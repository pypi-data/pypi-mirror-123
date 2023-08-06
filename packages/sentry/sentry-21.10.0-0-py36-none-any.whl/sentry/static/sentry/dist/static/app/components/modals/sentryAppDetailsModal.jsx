Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const circleIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/circleIndicator"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const pluginIcon_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/pluginIcon"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const consolidatedScopes_1 = require("app/utils/consolidatedScopes");
const integrationUtil_1 = require("app/utils/integrationUtil");
const marked_1 = (0, tslib_1.__importStar)(require("app/utils/marked"));
const recordSentryAppInteraction_1 = require("app/utils/recordSentryAppInteraction");
// No longer a modal anymore but yea :)
class SentryAppDetailsModal extends asyncComponent_1.default {
    componentDidUpdate(prevProps) {
        // if the user changes org, count this as a fresh event to track
        if (this.props.organization.id !== prevProps.organization.id) {
            this.trackOpened();
        }
    }
    componentDidMount() {
        this.trackOpened();
    }
    trackOpened() {
        const { sentryApp, organization, isInstalled } = this.props;
        (0, recordSentryAppInteraction_1.recordInteraction)(sentryApp.slug, 'sentry_app_viewed');
        (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.install_modal_opened', {
            integration_type: 'sentry_app',
            integration: sentryApp.slug,
            already_installed: isInstalled,
            view: 'external_install',
            integration_status: sentryApp.status,
            organization,
        }, { startSession: true });
    }
    getEndpoints() {
        const { sentryApp } = this.props;
        return [['featureData', `/sentry-apps/${sentryApp.slug}/features/`]];
    }
    featureTags(features) {
        return features.map(feature => {
            const feat = feature.featureGate.replace(/integrations/g, '');
            return <StyledTag key={feat}>{feat.replace(/-/g, ' ')}</StyledTag>;
        });
    }
    get permissions() {
        return (0, consolidatedScopes_1.toPermissions)(this.props.sentryApp.scopes);
    }
    onInstall() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { onInstall } = this.props;
            // we want to make sure install finishes before we close the modal
            // and we should close the modal if there is an error as well
            try {
                yield onInstall();
            }
            catch (_err) {
                /* stylelint-disable-next-line no-empty-block */
            }
        });
    }
    renderPermissions() {
        const permissions = this.permissions;
        if (Object.keys(permissions).filter(scope => permissions[scope].length > 0).length === 0) {
            return null;
        }
        return (<React.Fragment>
        <Title>Permissions</Title>
        {permissions.read.length > 0 && (<Permission>
            <Indicator />
            <Text key="read">
              {(0, locale_1.tct)('[read] access to [resources] resources', {
                    read: <strong>Read</strong>,
                    resources: permissions.read.join(', '),
                })}
            </Text>
          </Permission>)}
        {permissions.write.length > 0 && (<Permission>
            <Indicator />
            <Text key="write">
              {(0, locale_1.tct)('[read] and [write] access to [resources] resources', {
                    read: <strong>Read</strong>,
                    write: <strong>Write</strong>,
                    resources: permissions.write.join(', '),
                })}
            </Text>
          </Permission>)}
        {permissions.admin.length > 0 && (<Permission>
            <Indicator />
            <Text key="admin">
              {(0, locale_1.tct)('[admin] access to [resources] resources', {
                    admin: <strong>Admin</strong>,
                    resources: permissions.admin.join(', '),
                })}
            </Text>
          </Permission>)}
      </React.Fragment>);
    }
    renderBody() {
        const { sentryApp, closeModal, isInstalled, organization } = this.props;
        const { featureData } = this.state;
        // Prepare the features list
        const features = (featureData || []).map(f => ({
            featureGate: f.featureGate,
            description: (<span dangerouslySetInnerHTML={{ __html: (0, marked_1.singleLineRenderer)(f.description) }}/>),
        }));
        const { FeatureList, IntegrationFeatures } = (0, integrationUtil_1.getIntegrationFeatureGate)();
        const overview = sentryApp.overview || '';
        const featureProps = { organization, features };
        return (<React.Fragment>
        <Heading>
          <pluginIcon_1.default pluginId={sentryApp.slug} size={50}/>

          <HeadingInfo>
            <Name>{sentryApp.name}</Name>
            {!!features.length && <Features>{this.featureTags(features)}</Features>}
          </HeadingInfo>
        </Heading>

        <Description dangerouslySetInnerHTML={{ __html: (0, marked_1.default)(overview) }}/>
        <FeatureList {...featureProps} provider={Object.assign(Object.assign({}, sentryApp), { key: sentryApp.slug })}/>

        <IntegrationFeatures {...featureProps}>
          {({ disabled, disabledReason }) => (<React.Fragment>
              {!disabled && this.renderPermissions()}
              <Footer>
                <Author>{(0, locale_1.t)('Authored By %s', sentryApp.author)}</Author>
                <div>
                  {disabled && <DisabledNotice reason={disabledReason}/>}
                  <button_1.default size="small" onClick={closeModal}>
                    {(0, locale_1.t)('Cancel')}
                  </button_1.default>

                  <access_1.default organization={organization} access={['org:integrations']}>
                    {({ hasAccess }) => hasAccess && (<button_1.default size="small" priority="primary" disabled={isInstalled || disabled} onClick={() => this.onInstall()} style={{ marginLeft: (0, space_1.default)(1) }} data-test-id="install">
                          {(0, locale_1.t)('Accept & Install')}
                        </button_1.default>)}
                  </access_1.default>
                </div>
              </Footer>
            </React.Fragment>)}
        </IntegrationFeatures>
      </React.Fragment>);
    }
}
exports.default = SentryAppDetailsModal;
const Heading = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  margin-bottom: ${(0, space_1.default)(2)};
`;
const HeadingInfo = (0, styled_1.default)('div') `
  display: grid;
  grid-template-rows: max-content max-content;
  align-items: start;
`;
const Name = (0, styled_1.default)('div') `
  font-weight: bold;
  font-size: 1.4em;
`;
const Description = (0, styled_1.default)('div') `
  font-size: 1.5rem;
  line-height: 2.1rem;
  margin-bottom: ${(0, space_1.default)(2)};

  li {
    margin-bottom: 6px;
  }
`;
const Author = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
`;
const DisabledNotice = (0, styled_1.default)((_a) => {
    var { reason } = _a, p = (0, tslib_1.__rest)(_a, ["reason"]);
    return (<div {...p}>
    <icons_1.IconFlag color="red300" size="1.5em"/>
    {reason}
  </div>);
}) `
  display: grid;
  align-items: center;
  flex: 1;
  grid-template-columns: max-content 1fr;
  color: ${p => p.theme.red300};
  font-size: 0.9em;
`;
const Text = (0, styled_1.default)('p') `
  margin: 0px 6px;
`;
const Permission = (0, styled_1.default)('div') `
  display: flex;
`;
const Footer = (0, styled_1.default)('div') `
  display: flex;
  padding: 20px 30px;
  border-top: 1px solid #e2dee6;
  margin: 20px -30px -30px;
  justify-content: space-between;
`;
const Title = (0, styled_1.default)('p') `
  margin-bottom: ${(0, space_1.default)(1)};
  font-weight: bold;
`;
const Indicator = (0, styled_1.default)(p => <circleIndicator_1.default size={7} {...p}/>) `
  margin-top: 7px;
  color: ${p => p.theme.success};
`;
const Features = (0, styled_1.default)('div') `
  margin: -${(0, space_1.default)(0.5)};
`;
const StyledTag = (0, styled_1.default)(tag_1.default) `
  padding: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=sentryAppDetailsModal.jsx.map