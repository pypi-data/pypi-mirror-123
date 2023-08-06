Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const rangeSlider_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/rangeSlider"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
const RATE_LIMIT_FORMAT_MAP = new Map([
    [0, 'None'],
    [60, '1 minute'],
    [300, '5 minutes'],
    [900, '15 minutes'],
    [3600, '1 hour'],
    [7200, '2 hours'],
    [14400, '4 hours'],
    [21600, '6 hours'],
    [43200, '12 hours'],
    [86400, '24 hours'],
]);
// This value isn't actually any, but the various angles on the types don't line up.
const formatRateLimitWindow = (val) => RATE_LIMIT_FORMAT_MAP.get(val);
class KeyRateLimitsForm extends React.Component {
    constructor() {
        super(...arguments);
        this.handleChangeWindow = (onChange, onBlur, currentValueObj, value, e) => {
            const valueObj = Object.assign(Object.assign({}, currentValueObj), { window: value });
            onChange(valueObj, e);
            onBlur(valueObj, e);
        };
        this.handleChangeCount = (cb, value, e) => {
            const valueObj = Object.assign(Object.assign({}, value), { count: e.target.value });
            cb(valueObj, e);
        };
    }
    render() {
        const { data, disabled } = this.props;
        const { keyId, orgId, projectId } = this.props.params;
        const apiEndpoint = `/projects/${orgId}/${projectId}/keys/${keyId}/`;
        const disabledAlert = ({ features }) => (<featureDisabled_1.default alert={panels_1.PanelAlert} features={features} featureName={(0, locale_1.t)('Key Rate Limits')}/>);
        return (<form_1.default saveOnBlur apiEndpoint={apiEndpoint} apiMethod="PUT" initialData={data}>
        <feature_1.default features={['projects:rate-limits']} hookName="feature-disabled:rate-limits" renderDisabled={(_a) => {
                var { children } = _a, props = (0, tslib_1.__rest)(_a, ["children"]);
                return typeof children === 'function' &&
                    children(Object.assign(Object.assign({}, props), { renderDisabled: disabledAlert }));
            }}>
          {({ hasFeature, features, organization, project, renderDisabled }) => (<panels_1.Panel>
              <panels_1.PanelHeader>{(0, locale_1.t)('Rate Limits')}</panels_1.PanelHeader>

              <panels_1.PanelBody>
                <panels_1.PanelAlert type="info" icon={<icons_1.IconFlag size="md"/>}>
                  {(0, locale_1.t)(`Rate limits provide a flexible way to manage your error
                      volume. If you have a noisy project or environment you
                      can configure a rate limit for this key to reduce the
                      number of errors processed. To manage your transaction
                      volume, we recommend adjusting your sample rate in your
                      SDK configuration.`)}
                </panels_1.PanelAlert>
                {!hasFeature &&
                    typeof renderDisabled === 'function' &&
                    renderDisabled({
                        organization,
                        project,
                        features,
                        hasFeature,
                        children: null,
                    })}
                <formField_1.default className="rate-limit-group" name="rateLimit" label={(0, locale_1.t)('Rate Limit')} disabled={disabled || !hasFeature} validate={({ form }) => {
                    // TODO(TS): is validate actually doing anything because it's an unexpected prop
                    const isValid = form &&
                        form.rateLimit &&
                        typeof form.rateLimit.count !== 'undefined' &&
                        typeof form.rateLimit.window !== 'undefined';
                    if (isValid) {
                        return [];
                    }
                    return [['rateLimit', (0, locale_1.t)('Fill in both fields first')]];
                }} formatMessageValue={(value) => {
                    return (0, locale_1.t)('%s errors in %s', value.count, formatRateLimitWindow(value.window));
                }} help={(0, locale_1.t)('Apply a rate limit to this credential to cap the amount of errors accepted during a time window.')} inline={false}>
                  {({ onChange, onBlur, value }) => (<RateLimitRow>
                      <input_1.default type="number" name="rateLimit.count" min={0} value={value && value.count} placeholder={(0, locale_1.t)('Count')} disabled={disabled || !hasFeature} onChange={this.handleChangeCount.bind(this, onChange, value)} onBlur={this.handleChangeCount.bind(this, onBlur, value)}/>
                      <EventsIn>{(0, locale_1.t)('event(s) in')}</EventsIn>
                      <rangeSlider_1.default name="rateLimit.window" allowedValues={Array.from(RATE_LIMIT_FORMAT_MAP.keys())} value={value && value.window} placeholder={(0, locale_1.t)('Window')} formatLabel={formatRateLimitWindow} disabled={disabled || !hasFeature} onChange={this.handleChangeWindow.bind(this, onChange, onBlur, value)}/>
                    </RateLimitRow>)}
                </formField_1.default>
              </panels_1.PanelBody>
            </panels_1.Panel>)}
        </feature_1.default>
      </form_1.default>);
    }
}
exports.default = KeyRateLimitsForm;
const RateLimitRow = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 2fr 1fr 2fr;
  align-items: center;
  grid-gap: ${(0, space_1.default)(1)};
`;
const EventsIn = (0, styled_1.default)('small') `
  font-size: ${p => p.theme.fontSizeRelativeSmall};
  text-align: center;
  white-space: nowrap;
`;
//# sourceMappingURL=keyRateLimitsForm.jsx.map