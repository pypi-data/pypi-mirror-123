Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const issueAlertOptions_1 = require("app/views/projectInstall/issueAlertOptions");
const changeAlerts_1 = require("./constants/changeAlerts");
const ruleNode_1 = (0, tslib_1.__importDefault)(require("./ruleNode"));
class RuleNodeList extends React.Component {
    constructor() {
        super(...arguments);
        this.getNode = (id, itemIdx) => {
            const { nodes, items, organization } = this.props;
            const node = nodes ? nodes.find(n => n.id === id) : null;
            if (!node) {
                return null;
            }
            if (!organization.features.includes('change-alerts') ||
                !changeAlerts_1.CHANGE_ALERT_CONDITION_IDS.includes(node.id)) {
                return node;
            }
            const item = items[itemIdx];
            let changeAlertNode = Object.assign(Object.assign({}, node), { label: node.label.replace('...', ' {comparisonType}'), formFields: Object.assign(Object.assign({}, node.formFields), { comparisonType: {
                        type: 'choice',
                        choices: changeAlerts_1.COMPARISON_TYPE_CHOICES,
                        // give an initial value from not among choices so selector starts with none selected
                        initial: 'select',
                    } }) });
            if (item.comparisonType) {
                changeAlertNode = Object.assign(Object.assign({}, changeAlertNode), { label: changeAlertNode.label.replace('{comparisonType}', changeAlerts_1.COMPARISON_TYPE_CHOICE_VALUES[item.comparisonType]) });
                if (item.comparisonType === 'percent') {
                    changeAlertNode = Object.assign(Object.assign({}, changeAlertNode), { formFields: Object.assign(Object.assign({}, changeAlertNode.formFields), { comparisonInterval: {
                                type: 'choice',
                                choices: changeAlerts_1.COMPARISON_INTERVAL_CHOICES,
                                // comparisonInterval initial value isn't on the item, so it needs to be selected by user
                                initial: 'select',
                            } }) });
                }
            }
            return changeAlertNode;
        };
    }
    render() {
        var _a, _b;
        const { onAddRow, onResetRow, onDeleteRow, onPropertyChange, nodes, placeholder, items, organization, project, disabled, error, selectType, } = this.props;
        const shouldUsePrompt = (_b = (_a = project.features) === null || _a === void 0 ? void 0 : _a.includes) === null || _b === void 0 ? void 0 : _b.call(_a, 'issue-alerts-targeting');
        const enabledNodes = nodes ? nodes.filter(({ enabled }) => enabled) : [];
        const createSelectOptions = (actions) => actions.map(node => {
            var _a;
            const isNew = node.id === issueAlertOptions_1.EVENT_FREQUENCY_PERCENT_CONDITION;
            return {
                value: node.id,
                label: (<React.Fragment>
              {isNew && <StyledFeatureBadge type="new" noTooltip/>}
              {shouldUsePrompt && ((_a = node.prompt) === null || _a === void 0 ? void 0 : _a.length) > 0 ? node.prompt : node.label}
            </React.Fragment>),
            };
        });
        let options = !selectType ? createSelectOptions(enabledNodes) : [];
        if (selectType === 'grouped') {
            const grouped = enabledNodes.reduce((acc, curr) => {
                if (curr.actionType === 'ticket') {
                    acc.ticket.push(curr);
                }
                else {
                    acc.notify.push(curr);
                }
                return acc;
            }, {
                notify: [],
                ticket: [],
            });
            options = Object.entries(grouped)
                .filter(([_, values]) => values.length)
                .map(([key, values]) => {
                const label = key === 'ticket'
                    ? (0, locale_1.t)('Create new\u{2026}')
                    : (0, locale_1.t)('Send notification to\u{2026}');
                return { label, options: createSelectOptions(values) };
            });
        }
        return (<React.Fragment>
        <RuleNodes>
          {error}
          {items.map((item, idx) => (<ruleNode_1.default key={idx} index={idx} node={this.getNode(item.id, idx)} onDelete={onDeleteRow} onPropertyChange={onPropertyChange} onReset={onResetRow} data={item} organization={organization} project={project} disabled={disabled}/>))}
        </RuleNodes>
        <StyledSelectControl placeholder={placeholder} value={null} onChange={obj => onAddRow(obj ? obj.value : obj)} options={options} disabled={disabled}/>
      </React.Fragment>);
    }
}
exports.default = RuleNodeList;
const StyledSelectControl = (0, styled_1.default)(selectControl_1.default) `
  width: 100%;
`;
const RuleNodes = (0, styled_1.default)('div') `
  display: grid;
  margin-bottom: ${(0, space_1.default)(1)};
  grid-gap: ${(0, space_1.default)(1)};

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    grid-auto-flow: row;
  }
`;
const StyledFeatureBadge = (0, styled_1.default)(featureBadge_1.default) `
  margin: 0 ${(0, space_1.default)(1)} 0 0;
`;
//# sourceMappingURL=ruleNodeList.jsx.map