Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const panels_1 = require("app/components/panels");
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const ProviderItem = ({ provider, active, onConfigure }) => {
    const handleConfigure = (e) => {
        onConfigure === null || onConfigure === void 0 ? void 0 : onConfigure(provider.key, e);
    };
    const renderDisabledLock = (p) => (<LockedFeature provider={p.provider} features={p.features}/>);
    const defaultRenderInstallButton = ({ hasFeature }) => (<access_1.default access={['org:write']}>
      {({ hasAccess }) => (<button_1.default type="submit" name="provider" size="small" value={provider.key} disabled={!hasFeature || !hasAccess} onClick={handleConfigure}>
          {(0, locale_1.t)('Configure')}
        </button_1.default>)}
    </access_1.default>);
    // TODO(epurkhiser): We should probably use a more explicit hook name,
    // instead of just the feature names (sso-basic, sso-saml2, etc).
    const featureKey = provider.requiredFeature;
    const hookName = featureKey
        ? `feature-disabled:${(0, utils_1.descopeFeatureName)(featureKey)}`
        : null;
    const featureProps = hookName ? { hookName } : {};
    const getProviderDescription = providerName => {
        if (providerName === 'SAML2') {
            return (0, locale_1.t)('your preferred SAML2 compliant provider like Ping Identity, Google SAML, Keycloak, or VMware Identity Manager');
        }
        if (providerName === 'Google') {
            return (0, locale_1.t)('Google (OAuth)');
        }
        return providerName;
    };
    return (<feature_1.default {...featureProps} features={[featureKey].filter(f => f)} renderDisabled={(_a) => {
            var { children } = _a, props = (0, tslib_1.__rest)(_a, ["children"]);
            return typeof children === 'function' &&
                // TODO(ts): the Feature component isn't correctly templatized to allow
                // for custom props in the renderDisabled function
                children(Object.assign(Object.assign({}, props), { renderDisabled: renderDisabledLock }));
        }}>
      {({ hasFeature, features, renderDisabled, renderInstallButton, }) => (<panels_1.PanelItem center>
          <ProviderInfo>
            <ProviderLogo className={`provider-logo ${provider.name
                .replace(/\s/g, '-')
                .toLowerCase()}`}/>
            <div>
              <ProviderName>{provider.name}</ProviderName>
              <ProviderDescription>
                {(0, locale_1.t)('Enable your organization to sign in with %s.', getProviderDescription(provider.name))}
              </ProviderDescription>
            </div>
          </ProviderInfo>

          <FeatureBadge>
            {!hasFeature && renderDisabled({ provider, features })}
          </FeatureBadge>

          <div>
            {active ? (<ActiveIndicator />) : ((renderInstallButton !== null && renderInstallButton !== void 0 ? renderInstallButton : defaultRenderInstallButton)({ provider, hasFeature }))}
          </div>
        </panels_1.PanelItem>)}
    </feature_1.default>);
};
exports.default = ProviderItem;
const ProviderInfo = (0, styled_1.default)('div') `
  flex: 1;
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(2)};
`;
const ProviderLogo = (0, styled_1.default)('div') `
  height: 36px;
  width: 36px;
  border-radius: 3px;
  margin-right: 0;
  top: auto;
`;
const ProviderName = (0, styled_1.default)('div') `
  font-weight: bold;
`;
const ProviderDescription = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(0.75)};
  font-size: 0.8em;
`;
const FeatureBadge = (0, styled_1.default)('div') `
  flex: 1;
`;
const ActiveIndicator = (0, styled_1.default)('div') `
  background: ${p => p.theme.green300};
  color: ${p => p.theme.white};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(1.5)};
  border-radius: 2px;
  font-size: 0.8em;
`;
ActiveIndicator.defaultProps = {
    children: (0, locale_1.t)('Active'),
};
const DisabledHovercard = (0, styled_1.default)(hovercard_1.default) `
  width: 350px;
`;
const LockedFeature = ({ provider, features, className }) => (<DisabledHovercard containerClassName={className} body={<featureDisabled_1.default features={features} hideHelpToggle message={(0, locale_1.t)('%s SSO is disabled.', provider.name)} featureName={(0, locale_1.t)('SSO Auth')}/>}>
    <tag_1.default icon={<icons_1.IconLock />}>{(0, locale_1.t)('disabled')}</tag_1.default>
  </DisabledHovercard>);
//# sourceMappingURL=providerItem.jsx.map