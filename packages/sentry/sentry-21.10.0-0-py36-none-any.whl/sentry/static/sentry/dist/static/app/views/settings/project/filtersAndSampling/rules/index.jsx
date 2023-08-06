Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const indicator_1 = require("app/actionCreators/indicator");
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const dynamicSampling_1 = require("app/types/dynamicSampling");
const draggableList_1 = (0, tslib_1.__importDefault)(require("./draggableList"));
const rule_1 = (0, tslib_1.__importDefault)(require("./rule"));
const utils_1 = require("./utils");
class Rules extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.state = { rules: [] };
        this.handleUpdateRules = ({ activeIndex, overIndex, reorderedItems: ruleIds, }) => {
            const { rules } = this.state;
            const reorderedRules = ruleIds
                .map(ruleId => rules.find(rule => String(rule.id) === ruleId))
                .filter(rule => !!rule);
            const activeRuleType = rules[activeIndex].type;
            const overRuleType = rules[overIndex].type;
            if (activeRuleType === dynamicSampling_1.DynamicSamplingRuleType.TRACE &&
                overRuleType === dynamicSampling_1.DynamicSamplingRuleType.TRANSACTION) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Transaction traces rules cannot be under individual transactions rules'));
                return;
            }
            if (activeRuleType === dynamicSampling_1.DynamicSamplingRuleType.TRANSACTION &&
                overRuleType === dynamicSampling_1.DynamicSamplingRuleType.TRACE) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Individual transactions rules cannot be above transaction traces rules'));
                return;
            }
            this.setState({ rules: reorderedRules });
        };
    }
    componentDidMount() {
        this.getRules();
    }
    componentDidUpdate(prevProps) {
        if (!(0, isEqual_1.default)(prevProps.rules, this.props.rules)) {
            this.getRules();
            return;
        }
        if (!(0, isEqual_1.default)(this.props.rules, this.state.rules)) {
            this.handleUpdateRulesParent();
        }
    }
    getRules() {
        this.setState({ rules: this.props.rules });
    }
    handleUpdateRulesParent() {
        const { onUpdateRules } = this.props;
        const { rules } = this.state;
        onUpdateRules(rules);
    }
    render() {
        const { onEditRule, onDeleteRule, disabled, emptyMessage } = this.props;
        const { rules } = this.state;
        return (<StyledPanelTable headers={['', (0, locale_1.t)('Type'), (0, locale_1.t)('Conditions'), (0, locale_1.t)('Rate'), '']} isEmpty={!rules.length} emptyMessage={emptyMessage}>
        <draggableList_1.default disabled={disabled} items={rules.map(rule => String(rule.id))} onUpdateItems={this.handleUpdateRules} wrapperStyle={({ isDragging, isSorting, index }) => {
                if (isDragging) {
                    return {
                        cursor: 'grabbing',
                    };
                }
                if (isSorting) {
                    return {};
                }
                return {
                    transform: 'none',
                    transformOrigin: '0',
                    '--box-shadow': 'none',
                    '--box-shadow-picked-up': 'none',
                    overflow: 'visible',
                    position: 'relative',
                    zIndex: rules.length - index,
                    cursor: 'default',
                };
            }} renderItem={({ value, listeners, attributes, dragging, sorting }) => {
                const currentRule = rules.find(rule => String(rule.id) === value);
                if (!currentRule) {
                    return null;
                }
                return (<rule_1.default rule={currentRule} onEditRule={onEditRule(currentRule)} onDeleteRule={onDeleteRule(currentRule)} disabled={disabled} listeners={listeners} grabAttributes={attributes} dragging={dragging} sorting={sorting}/>);
            }}/>
      </StyledPanelTable>);
    }
}
exports.default = Rules;
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  overflow: visible;
  margin-bottom: 0;
  border: none;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  ${p => (0, utils_1.layout)(p.theme)}
  > * {
    ${overflowEllipsis_1.default};
    :not(:last-child) {
      border-bottom: 1px solid ${p => p.theme.border};
    }
    :nth-child(n + 6) {
      ${p => !p.isEmpty
    ? `
              display: grid;
              grid-column: 1/-1;
              padding: 0;
            `
    : `
              display: block;
              grid-column: 1/-1;
            `}
    }
  }
`;
//# sourceMappingURL=index.jsx.map