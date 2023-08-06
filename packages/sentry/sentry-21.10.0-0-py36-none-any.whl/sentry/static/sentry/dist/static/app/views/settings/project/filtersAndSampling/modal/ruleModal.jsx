Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const iconCheckmark_1 = require("app/icons/iconCheckmark");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dynamicSampling_1 = require("app/types/dynamicSampling");
const utils_1 = require("app/utils");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const numberField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/numberField"));
const conditions_1 = (0, tslib_1.__importDefault)(require("./conditions"));
const handleXhrErrorResponse_1 = (0, tslib_1.__importDefault)(require("./handleXhrErrorResponse"));
const utils_2 = require("./utils");
function RuleModal({ Header, Body, Footer, closeModal, title, emptyMessage, conditionCategories, api, organization, project, onSubmitSuccess, onSubmit, onChange, extraFields, rule, }) {
    const [data, setData] = (0, react_1.useState)(getInitialState());
    (0, react_1.useEffect)(() => {
        if (!!data.errors.sampleRate) {
            setData(Object.assign(Object.assign({}, data), { errors: Object.assign(Object.assign({}, data.errors), { sampleRate: undefined }) }));
        }
    }, [data.sampleRate]);
    (0, react_1.useEffect)(() => {
        onChange === null || onChange === void 0 ? void 0 : onChange(data);
    }, [data]);
    function getInitialState() {
        if (rule) {
            const { condition: conditions, sampleRate } = rule;
            const { inner } = conditions;
            return {
                conditions: inner.map(({ name, value }) => {
                    if (Array.isArray(value)) {
                        if ((0, utils_2.isLegacyBrowser)(value)) {
                            return {
                                category: name,
                                legacyBrowsers: value,
                            };
                        }
                        return {
                            category: name,
                            match: value.join('\n'),
                        };
                    }
                    return { category: name };
                }),
                sampleRate: sampleRate * 100,
                errors: {},
            };
        }
        return {
            conditions: [],
            sampleRate: null,
            errors: {},
        };
    }
    const { errors, conditions, sampleRate } = data;
    function submitRules(newRules, currentRuleIndex) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                const newProjectDetails = yield api.requestPromise(`/projects/${organization.slug}/${project.slug}/`, { method: 'PUT', data: { dynamicSampling: { rules: newRules } } });
                onSubmitSuccess(newProjectDetails, rule
                    ? (0, locale_1.t)('Successfully edited dynamic sampling rule')
                    : (0, locale_1.t)('Successfully added dynamic sampling rule'));
                closeModal();
            }
            catch (error) {
                convertErrorXhrResponse((0, handleXhrErrorResponse_1.default)(error, currentRuleIndex));
            }
        });
    }
    function convertErrorXhrResponse(error) {
        switch (error.type) {
            case 'sampleRate':
                setData(Object.assign(Object.assign({}, data), { errors: Object.assign(Object.assign({}, errors), { sampleRate: error.message }) }));
                break;
            default:
                (0, indicator_1.addErrorMessage)(error.message);
        }
    }
    function handleAddCondition(category) {
        setData(Object.assign(Object.assign({}, data), { conditions: [
                ...conditions,
                {
                    category,
                    match: '',
                },
            ] }));
    }
    function handleDeleteCondition(index) {
        const newConditions = [...conditions];
        newConditions.splice(index, 1);
        setData(Object.assign(Object.assign({}, data), { conditions: newConditions }));
    }
    function handleChangeCondition(index, field, value) {
        const newConditions = [...conditions];
        newConditions[index][field] = value;
        setData(Object.assign(Object.assign({}, data), { conditions: newConditions }));
    }
    const submitDisabled = !(0, utils_1.defined)(sampleRate) ||
        !!(conditions === null || conditions === void 0 ? void 0 : conditions.find(condition => {
            var _a;
            if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER) {
                return !((_a = condition.legacyBrowsers) !== null && _a !== void 0 ? _a : []).length;
            }
            if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST ||
                condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS ||
                condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS) {
                return false;
            }
            return !condition.match;
        }));
    return (<react_1.Fragment>
      <Header closeButton>
        <h4>{title}</h4>
      </Header>
      <Body>
        <Fields>
          {extraFields}
          <StyledPanel>
            <StyledPanelHeader hasButtons>
              {(0, locale_1.t)('Conditions')}
              <dropdownAutoComplete_1.default onSelect={item => {
            handleAddCondition(item.value);
        }} alignMenu="right" items={conditionCategories.map(conditionCategory => {
            const disabled = conditions.some(condition => condition.category === conditionCategory[0]);
            return {
                value: conditionCategory[0],
                disabled,
                label: (<tooltip_1.default title={(0, locale_1.t)('This condition has already been added')} disabled={!disabled}>
                        <StyledMenuItem disabled={disabled}>
                          {conditionCategory[1]}
                        </StyledMenuItem>
                      </tooltip_1.default>),
            };
        })}>
                {({ isOpen }) => (<dropdownButton_1.default isOpen={isOpen} size="small">
                    {(0, locale_1.t)('Add Condition')}
                  </dropdownButton_1.default>)}
              </dropdownAutoComplete_1.default>
            </StyledPanelHeader>
            <panels_1.PanelBody>
              {!conditions.length ? (<emptyMessage_1.default icon={<iconCheckmark_1.IconCheckmark isCircled size="xl"/>}>
                  {emptyMessage}
                </emptyMessage_1.default>) : (<conditions_1.default conditions={conditions} onDelete={handleDeleteCondition} onChange={handleChangeCondition} orgSlug={organization.slug} projectId={project.id}/>)}
            </panels_1.PanelBody>
          </StyledPanel>
          <numberField_1.default label={`${(0, locale_1.t)('Sampling Rate')} \u0025`} name="sampleRate" onChange={value => {
            setData(Object.assign(Object.assign({}, data), { sampleRate: !!value ? Number(value) : null }));
        }} placeholder={'\u0025'} value={sampleRate} inline={false} hideControlState={!errors.sampleRate} error={errors.sampleRate} showHelpInTooltip stacked required/>
        </Fields>
      </Body>
      <Footer>
        <buttonBar_1.default gap={1}>
          <button_1.default onClick={closeModal}>{(0, locale_1.t)('Cancel')}</button_1.default>
          <button_1.default priority="primary" onClick={() => onSubmit({ conditions, sampleRate, submitRules })} title={submitDisabled ? (0, locale_1.t)('Required fields must be filled out') : undefined} disabled={submitDisabled}>
            {(0, locale_1.t)('Save Rule')}
          </button_1.default>
        </buttonBar_1.default>
      </Footer>
    </react_1.Fragment>);
}
exports.default = RuleModal;
const Fields = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};
`;
const StyledMenuItem = (0, styled_1.default)(menuItem_1.default) `
  color: ${p => p.theme.textColor};
  font-size: ${p => p.theme.fontSizeMedium};
  font-weight: 400;
  text-transform: none;
  span {
    padding: 0;
  }
`;
const StyledPanelHeader = (0, styled_1.default)(panels_1.PanelHeader) `
  padding-right: ${(0, space_1.default)(2)};
`;
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  margin-bottom: 0;
`;
//# sourceMappingURL=ruleModal.jsx.map