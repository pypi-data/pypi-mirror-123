Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const indicator_1 = require("app/actionCreators/indicator");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const environment_1 = require("app/utils/environment");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const utils_1 = require("app/views/alerts/utils");
const options_1 = require("app/views/alerts/wizard/options");
const radioGroup_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/radioGroup"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
const constants_1 = require("./constants");
const metricField_1 = (0, tslib_1.__importDefault)(require("./metricField"));
const types_1 = require("./types");
const TIME_WINDOW_MAP = {
    [types_1.TimeWindow.ONE_MINUTE]: (0, locale_1.t)('1 minute'),
    [types_1.TimeWindow.FIVE_MINUTES]: (0, locale_1.t)('5 minutes'),
    [types_1.TimeWindow.TEN_MINUTES]: (0, locale_1.t)('10 minutes'),
    [types_1.TimeWindow.FIFTEEN_MINUTES]: (0, locale_1.t)('15 minutes'),
    [types_1.TimeWindow.THIRTY_MINUTES]: (0, locale_1.t)('30 minutes'),
    [types_1.TimeWindow.ONE_HOUR]: (0, locale_1.t)('1 hour'),
    [types_1.TimeWindow.TWO_HOURS]: (0, locale_1.t)('2 hours'),
    [types_1.TimeWindow.FOUR_HOURS]: (0, locale_1.t)('4 hours'),
    [types_1.TimeWindow.ONE_DAY]: (0, locale_1.t)('24 hours'),
};
class RuleConditionsForm extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            environments: null,
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    fetchData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, projectSlug } = this.props;
            try {
                const environments = yield api.requestPromise(`/projects/${organization.slug}/${projectSlug}/environments/`, {
                    query: {
                        visibility: 'visible',
                    },
                });
                this.setState({ environments });
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to fetch environments'));
            }
        });
    }
    get timeWindowOptions() {
        let options = TIME_WINDOW_MAP;
        if (this.props.dataset === types_1.Dataset.SESSIONS) {
            options = (0, pick_1.default)(TIME_WINDOW_MAP, [
                // TimeWindow.THIRTY_MINUTES, leaving this option out until we figure out the sub-hour session resolution chart limitations
                types_1.TimeWindow.ONE_HOUR,
                types_1.TimeWindow.TWO_HOURS,
                types_1.TimeWindow.FOUR_HOURS,
                types_1.TimeWindow.ONE_DAY,
            ]);
        }
        return Object.entries(options).map(([value, label]) => ({
            value,
            label,
        }));
    }
    get searchPlaceholder() {
        switch (this.props.dataset) {
            case types_1.Dataset.ERRORS:
                return (0, locale_1.t)('Filter events by level, message, and other properties\u2026');
            case types_1.Dataset.SESSIONS:
                return (0, locale_1.t)('Filter sessions by release version\u2026');
            case types_1.Dataset.TRANSACTIONS:
            default:
                return (0, locale_1.t)('Filter transactions by URL, tags, and other properties\u2026');
        }
    }
    get searchSupportedTags() {
        if (this.props.dataset === types_1.Dataset.SESSIONS) {
            return {
                release: {
                    key: 'release',
                    name: 'release',
                },
            };
        }
        return undefined;
    }
    render() {
        var _a;
        const { organization, disabled, onFilterSearch, allowChangeEventTypes, alertType, comparisonType, comparisonDelta, onComparisonDeltaChange, onComparisonTypeChange, dataset, } = this.props;
        const { environments } = this.state;
        const environmentOptions = (_a = environments === null || environments === void 0 ? void 0 : environments.map((env) => ({
            value: env.name,
            label: (0, environment_1.getDisplayName)(env),
        }))) !== null && _a !== void 0 ? _a : [];
        const anyEnvironmentLabel = (<React.Fragment>
        {(0, locale_1.t)('All')}
        <div className="all-environment-note">
          {(0, locale_1.tct)(`This will count events across every environment. For example,
             having 50 [code1:production] events and 50 [code2:development]
             events would trigger an alert with a critical threshold of 100.`, { code1: <code />, code2: <code /> })}
        </div>
      </React.Fragment>);
        environmentOptions.unshift({ value: null, label: anyEnvironmentLabel });
        const dataSourceOptions = [
            {
                label: (0, locale_1.t)('Errors'),
                options: [
                    {
                        value: types_1.Datasource.ERROR_DEFAULT,
                        label: utils_1.DATA_SOURCE_LABELS[types_1.Datasource.ERROR_DEFAULT],
                    },
                    {
                        value: types_1.Datasource.DEFAULT,
                        label: utils_1.DATA_SOURCE_LABELS[types_1.Datasource.DEFAULT],
                    },
                    {
                        value: types_1.Datasource.ERROR,
                        label: utils_1.DATA_SOURCE_LABELS[types_1.Datasource.ERROR],
                    },
                ],
            },
        ];
        if (organization.features.includes('performance-view') && alertType === 'custom') {
            dataSourceOptions.push({
                label: (0, locale_1.t)('Transactions'),
                options: [
                    {
                        value: types_1.Datasource.TRANSACTION,
                        label: utils_1.DATA_SOURCE_LABELS[types_1.Datasource.TRANSACTION],
                    },
                ],
            });
        }
        const formElemBaseStyle = {
            padding: `${(0, space_1.default)(0.5)}`,
            border: 'none',
        };
        const { labelText: intervalLabelText, timeWindowText } = (0, options_1.getFunctionHelpText)(alertType);
        return (<React.Fragment>
        <ChartPanel>
          <StyledPanelBody>{this.props.thresholdChart}</StyledPanelBody>
        </ChartPanel>
        <StyledListItem>{(0, locale_1.t)('Filter events')}</StyledListItem>
        <FormRow>
          <selectField_1.default name="environment" placeholder={(0, locale_1.t)('All')} style={Object.assign(Object.assign({}, formElemBaseStyle), { minWidth: 180, flex: 1 })} styles={{
                singleValue: (base) => (Object.assign(Object.assign({}, base), { '.all-environment-note': { display: 'none' } })),
                option: (base, state) => (Object.assign(Object.assign({}, base), { '.all-environment-note': Object.assign(Object.assign({}, (!state.isSelected && !state.isFocused
                        ? { color: theme_1.default.gray400 }
                        : {})), { fontSize: theme_1.default.fontSizeSmall }) })),
            }} options={environmentOptions} isDisabled={disabled || this.state.environments === null} isClearable inline={false} flexibleControlStateSize inFieldLabel={(0, locale_1.t)('Env: ')}/>
          {allowChangeEventTypes && (<formField_1.default name="datasource" inline={false} style={Object.assign(Object.assign({}, formElemBaseStyle), { minWidth: 300, flex: 2 })} flexibleControlStateSize>
              {({ onChange, onBlur, model }) => {
                    const formDataset = model.getValue('dataset');
                    const formEventTypes = model.getValue('eventTypes');
                    const mappedValue = (0, utils_1.convertDatasetEventTypesToSource)(formDataset, formEventTypes);
                    return (<selectControl_1.default value={mappedValue} inFieldLabel={(0, locale_1.t)('Events: ')} onChange={optionObj => {
                            var _a;
                            const optionValue = optionObj.value;
                            onChange(optionValue, {});
                            onBlur(optionValue, {});
                            // Reset the aggregate to the default (which works across
                            // datatypes), otherwise we may send snuba an invalid query
                            // (transaction aggregate on events datasource = bad).
                            optionValue === 'transaction'
                                ? model.setValue('aggregate', constants_1.DEFAULT_TRANSACTION_AGGREGATE)
                                : model.setValue('aggregate', constants_1.DEFAULT_AGGREGATE);
                            // set the value of the dataset and event type from data source
                            const { dataset: datasetFromDataSource, eventTypes } = (_a = utils_1.DATA_SOURCE_TO_SET_AND_EVENT_TYPES[optionValue]) !== null && _a !== void 0 ? _a : {};
                            model.setValue('dataset', datasetFromDataSource);
                            model.setValue('eventTypes', eventTypes);
                        }} options={dataSourceOptions} isDisabled={disabled}/>);
                }}
            </formField_1.default>)}
          <formField_1.default name="query" inline={false} style={Object.assign(Object.assign({}, formElemBaseStyle), { flex: '6 0 500px' })} flexibleControlStateSize>
            {({ onChange, onBlur, onKeyDown, initialData }) => {
                var _a;
                return (<SearchContainer>
                <StyledSearchBar searchSource="alert_builder" defaultQuery={(_a = initialData === null || initialData === void 0 ? void 0 : initialData.query) !== null && _a !== void 0 ? _a : ''} omitTags={['event.type']} disabled={disabled} useFormWrapper={false} organization={organization} placeholder={this.searchPlaceholder} onChange={onChange} onKeyDown={e => {
                        /**
                         * Do not allow enter key to submit the alerts form since it is unlikely
                         * users will be ready to create the rule as this sits above required fields.
                         */
                        if (e.key === 'Enter') {
                            e.preventDefault();
                            e.stopPropagation();
                        }
                        onKeyDown === null || onKeyDown === void 0 ? void 0 : onKeyDown(e);
                    }} onBlur={query => {
                        onFilterSearch(query);
                        onBlur(query);
                    }} onSearch={query => {
                        onFilterSearch(query);
                        onChange(query, {});
                    }} {...(this.searchSupportedTags
                    ? { supportedTags: this.searchSupportedTags }
                    : {})} hasRecentSearches={dataset !== types_1.Dataset.SESSIONS}/>
              </SearchContainer>);
            }}
          </formField_1.default>
        </FormRow>
        {dataset !== types_1.Dataset.SESSIONS && (<feature_1.default features={['organizations:change-alerts']} organization={organization}>
            <StyledListItem>{(0, locale_1.t)('Select threshold type')}</StyledListItem>
            <FormRow>
              <radioGroup_1.default style={{ flex: 1 }} choices={[
                    [types_1.AlertRuleComparisonType.COUNT, 'Count'],
                    [types_1.AlertRuleComparisonType.CHANGE, 'Percent Change'],
                ]} value={comparisonType} label={(0, locale_1.t)('Threshold Type')} onChange={onComparisonTypeChange}/>
            </FormRow>
          </feature_1.default>)}
        <StyledListItem>
          <StyledListTitle>
            <div>{intervalLabelText}</div>
            <tooltip_1.default title={(0, locale_1.t)('Time window over which the metric is evaluated. Alerts are evaluated every minute regardless of this value.')}>
              <icons_1.IconQuestion size="sm" color="gray200"/>
            </tooltip_1.default>
          </StyledListTitle>
        </StyledListItem>
        <FormRow>
          {timeWindowText && (<metricField_1.default name="aggregate" help={null} organization={organization} disabled={disabled} style={Object.assign({}, formElemBaseStyle)} inline={false} flexibleControlStateSize columnWidth={200} alertType={alertType} required/>)}
          {timeWindowText && <FormRowText>{timeWindowText}</FormRowText>}
          <selectField_1.default name="timeWindow" style={Object.assign(Object.assign({}, formElemBaseStyle), { flex: '0 150px 0', minWidth: 130, maxWidth: 300 })} options={this.timeWindowOptions} required isDisabled={disabled} getValue={value => Number(value)} setValue={value => `${value}`} inline={false} flexibleControlStateSize/>
          <feature_1.default features={['organizations:change-alerts']} organization={organization}>
            {comparisonType === types_1.AlertRuleComparisonType.CHANGE && (<ComparisonContainer>
                {(0, locale_1.t)(' compared to ')}
                <selectField_1.default name="comparisonDelta" style={Object.assign(Object.assign({}, formElemBaseStyle), { minWidth: 500, maxWidth: 1000 })} value={comparisonDelta} onChange={onComparisonDeltaChange} options={constants_1.COMPARISON_DELTA_OPTIONS} required={comparisonType === types_1.AlertRuleComparisonType.CHANGE}/>
              </ComparisonContainer>)}
          </feature_1.default>
        </FormRow>
      </React.Fragment>);
    }
}
const StyledListTitle = (0, styled_1.default)('div') `
  display: flex;
  span {
    margin-left: ${(0, space_1.default)(1)};
  }
`;
const ChartPanel = (0, styled_1.default)(panels_1.Panel) `
  margin-bottom: ${(0, space_1.default)(4)};
`;
const StyledPanelBody = (0, styled_1.default)(panels_1.PanelBody) `
  ol,
  h4 {
    margin-bottom: ${(0, space_1.default)(1)};
  }
`;
const SearchContainer = (0, styled_1.default)('div') `
  display: flex;
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
`;
const StyledListItem = (0, styled_1.default)(listItem_1.default) `
  margin-bottom: ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeExtraLarge};
  line-height: 1.3;
`;
const FormRow = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: ${(0, space_1.default)(4)};
`;
const FormRowText = (0, styled_1.default)('div') `
  margin: ${(0, space_1.default)(1)};
`;
const ComparisonContainer = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(1)};
  display: flex;
  flex-direction: row;
  align-items: center;
`;
exports.default = RuleConditionsForm;
//# sourceMappingURL=ruleConditionsForm.jsx.map