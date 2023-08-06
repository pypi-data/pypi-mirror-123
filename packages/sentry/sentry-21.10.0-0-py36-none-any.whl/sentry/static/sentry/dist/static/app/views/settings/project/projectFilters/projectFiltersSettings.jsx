Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const panels_1 = require("app/components/panels");
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const inboundFilters_1 = (0, tslib_1.__importStar)(require("app/data/forms/inboundFilters"));
const locale_1 = require("app/locale");
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const fieldFromConfig_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/fieldFromConfig"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const LEGACY_BROWSER_SUBFILTERS = {
    ie_pre_9: {
        icon: 'internet-explorer',
        helpText: 'Version 8 and lower',
        title: 'Internet Explorer',
    },
    ie9: {
        icon: 'internet-explorer',
        helpText: 'Version 9',
        title: 'Internet Explorer',
    },
    ie10: {
        icon: 'internet-explorer',
        helpText: 'Version 10',
        title: 'Internet Explorer',
    },
    ie11: {
        icon: 'internet-explorer',
        helpText: 'Version 11',
        title: 'Internet Explorer',
    },
    safari_pre_6: {
        icon: 'safari',
        helpText: 'Version 5 and lower',
        title: 'Safari',
    },
    opera_pre_15: {
        icon: 'opera',
        helpText: 'Version 14 and lower',
        title: 'Opera',
    },
    opera_mini_pre_8: {
        icon: 'opera',
        helpText: 'Version 8 and lower',
        title: 'Opera Mini',
    },
    android_pre_4: {
        icon: 'android',
        helpText: 'Version 3 and lower',
        title: 'Android',
    },
};
const LEGACY_BROWSER_KEYS = Object.keys(LEGACY_BROWSER_SUBFILTERS);
class LegacyBrowserFilterRow extends React.Component {
    constructor(props) {
        super(props);
        this.handleToggleSubfilters = (subfilter, e) => {
            let { subfilters } = this.state;
            if (subfilter === true) {
                subfilters = new Set(LEGACY_BROWSER_KEYS);
            }
            else if (subfilter === false) {
                subfilters = new Set();
            }
            else if (subfilters.has(subfilter)) {
                subfilters.delete(subfilter);
            }
            else {
                subfilters.add(subfilter);
            }
            this.setState({
                subfilters: new Set(subfilters),
            }, () => {
                this.props.onToggle(this.props.data, subfilters, e);
            });
        };
        let initialSubfilters;
        if (props.data.active === true) {
            initialSubfilters = new Set(LEGACY_BROWSER_KEYS);
        }
        else if (props.data.active === false) {
            initialSubfilters = new Set();
        }
        else {
            initialSubfilters = new Set(props.data.active);
        }
        this.state = {
            loading: false,
            error: false,
            subfilters: initialSubfilters,
        };
    }
    render() {
        const { disabled } = this.props;
        return (<div>
        {!disabled && (<BulkFilter>
            <BulkFilterLabel>{(0, locale_1.t)('Filter')}:</BulkFilterLabel>
            <BulkFilterItem onClick={this.handleToggleSubfilters.bind(this, true)}>
              {(0, locale_1.t)('All')}
            </BulkFilterItem>
            <BulkFilterItem onClick={this.handleToggleSubfilters.bind(this, false)}>
              {(0, locale_1.t)('None')}
            </BulkFilterItem>
          </BulkFilter>)}

        <FilterGrid>
          {LEGACY_BROWSER_KEYS.map(key => {
                const subfilter = LEGACY_BROWSER_SUBFILTERS[key];
                return (<FilterGridItemWrapper key={key}>
                <FilterGridItem>
                  <FilterItem>
                    <FilterGridIcon className={`icon-${subfilter.icon}`}/>
                    <div>
                      <FilterTitle>{subfilter.title}</FilterTitle>
                      <FilterDescription>{subfilter.helpText}</FilterDescription>
                    </div>
                  </FilterItem>

                  <switchButton_1.default isActive={this.state.subfilters.has(key)} isDisabled={disabled} css={{ flexShrink: 0, marginLeft: 6 }} toggle={this.handleToggleSubfilters.bind(this, key)} size="lg"/>
                </FilterGridItem>
              </FilterGridItemWrapper>);
            })}
        </FilterGrid>
      </div>);
    }
}
class ProjectFiltersSettings extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleLegacyChange = (onChange, onBlur, _filter, subfilters, e) => {
            onChange === null || onChange === void 0 ? void 0 : onChange(subfilters, e);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(subfilters, e);
        };
        this.handleSubmit = (response) => {
            // This will update our project context
            projectActions_1.default.updateSuccess(response);
        };
        this.renderDisabledCustomFilters = p => (<featureDisabled_1.default featureName={(0, locale_1.t)('Custom Inbound Filters')} features={p.features} alert={panels_1.PanelAlert} message={(0, locale_1.t)('Release and Error Message filtering are not enabled on your Sentry installation')}/>);
        this.renderCustomFilters = (disabled) => () => (<feature_1.default features={['projects:custom-inbound-filters']} hookName="feature-disabled:custom-inbound-filters" renderDisabled={(_a) => {
                var { children } = _a, props = (0, tslib_1.__rest)(_a, ["children"]);
                if (typeof children === 'function') {
                    return children(Object.assign(Object.assign({}, props), { renderDisabled: this.renderDisabledCustomFilters }));
                }
                return null;
            }}>
        {(_a) => {
                var _b;
                var { hasFeature, organization, renderDisabled } = _a, featureProps = (0, tslib_1.__rest)(_a, ["hasFeature", "organization", "renderDisabled"]);
                return (<React.Fragment>
            {!hasFeature &&
                        typeof renderDisabled === 'function' &&
                        // XXX: children is set to null as we're doing tricksy things
                        // in the renderDisabled prop a few lines higher.
                        renderDisabled(Object.assign({ organization, hasFeature, children: null }, featureProps))}

            {inboundFilters_1.customFilterFields.map(field => (<fieldFromConfig_1.default key={field.name} field={field} disabled={disabled || !hasFeature}/>))}

            {hasFeature && ((_b = this.props.project.options) === null || _b === void 0 ? void 0 : _b['filters:error_messages']) && (<panels_1.PanelAlert type="warning" data-test-id="error-message-disclaimer">
                {(0, locale_1.t)("Minidumps, errors in the minified production build of React, and Internet Explorer's i18n errors cannot be filtered by message.")}
              </panels_1.PanelAlert>)}
          </React.Fragment>);
            }}
      </feature_1.default>);
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { hooksDisabled: hookStore_1.default.get('feature-disabled:custom-inbound-filters') });
    }
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [['filterList', `/projects/${orgId}/${projectId}/filters/`]];
    }
    componentDidUpdate(prevProps, prevState) {
        if (prevProps.project.slug !== this.props.project.slug) {
            this.reloadData();
        }
        super.componentDidUpdate(prevProps, prevState);
    }
    renderBody() {
        const { features, params, project } = this.props;
        const { orgId, projectId } = params;
        const projectEndpoint = `/projects/${orgId}/${projectId}/`;
        const filtersEndpoint = `${projectEndpoint}filters/`;
        return (<access_1.default access={['project:write']}>
        {({ hasAccess }) => (<React.Fragment>
            <panels_1.Panel>
              <panels_1.PanelHeader>{(0, locale_1.t)('Filters')}</panels_1.PanelHeader>
              <panels_1.PanelBody>
                {this.state.filterList.map(filter => {
                    const fieldProps = {
                        name: filter.id,
                        label: filter.name,
                        help: filter.description,
                        disabled: !hasAccess,
                    };
                    // Note by default, forms generate data in the format of:
                    // { [fieldName]: [value] }
                    // Endpoints for these filters expect data to be:
                    // { 'active': [value] }
                    return (<panels_1.PanelItem key={filter.id} noPadding>
                      <NestedForm apiMethod="PUT" apiEndpoint={`${filtersEndpoint}${filter.id}/`} initialData={{ [filter.id]: filter.active }} saveOnBlur>
                        {filter.id !== 'legacy-browsers' ? (<fieldFromConfig_1.default key={filter.id} getData={data => ({ active: data[filter.id] })} field={Object.assign({ type: 'boolean' }, fieldProps)}/>) : (<formField_1.default inline={false} {...fieldProps} getData={data => ({ subfilters: [...data[filter.id]] })}>
                            {({ onChange, onBlur }) => (<LegacyBrowserFilterRow key={filter.id} data={filter} disabled={!hasAccess} onToggle={this.handleLegacyChange.bind(this, onChange, onBlur)}/>)}
                          </formField_1.default>)}
                      </NestedForm>
                    </panels_1.PanelItem>);
                })}
              </panels_1.PanelBody>
            </panels_1.Panel>

            <form_1.default apiMethod="PUT" apiEndpoint={projectEndpoint} initialData={project.options} saveOnBlur onSubmitSuccess={this.handleSubmit}>
              <jsonForm_1.default features={features} forms={inboundFilters_1.default} disabled={!hasAccess} renderFooter={this.renderCustomFilters(!hasAccess)}/>
            </form_1.default>
          </React.Fragment>)}
      </access_1.default>);
    }
}
exports.default = ProjectFiltersSettings;
// TODO(ts): Understand why styled is not correctly inheriting props here
const NestedForm = (0, styled_1.default)(form_1.default) `
  flex: 1;
`;
const FilterGrid = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
`;
const FilterGridItem = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  background: ${p => p.theme.backgroundSecondary};
  border-radius: 3px;
  flex: 1;
  padding: 12px;
  height: 100%;
`;
// We want this wrapper to maining 30% width
const FilterGridItemWrapper = (0, styled_1.default)('div') `
  padding: 12px;
  width: 50%;
`;
const FilterItem = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  align-items: center;
`;
const FilterGridIcon = (0, styled_1.default)('div') `
  width: 38px;
  height: 38px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: 38px 38px;
  margin-right: 6px;
  flex-shrink: 0;
`;
const FilterTitle = (0, styled_1.default)('div') `
  font-size: 14px;
  font-weight: bold;
  line-height: 1;
  white-space: nowrap;
`;
const FilterDescription = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  font-size: 12px;
  line-height: 1;
  white-space: nowrap;
`;
const BulkFilter = (0, styled_1.default)('div') `
  text-align: right;
  padding: 0 12px;
`;
const BulkFilterLabel = (0, styled_1.default)('span') `
  font-weight: bold;
  margin-right: 6px;
`;
const BulkFilterItem = (0, styled_1.default)('a') `
  border-right: 1px solid #f1f2f3;
  margin-right: 6px;
  padding-right: 6px;

  &:last-child {
    border-right: none;
    margin-right: 0;
  }
`;
//# sourceMappingURL=projectFiltersSettings.jsx.map