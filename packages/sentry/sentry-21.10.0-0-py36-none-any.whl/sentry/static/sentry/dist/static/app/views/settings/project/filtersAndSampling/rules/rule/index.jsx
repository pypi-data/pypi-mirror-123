Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const iconGrabbable_1 = require("app/icons/iconGrabbable");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("../utils");
const actions_1 = (0, tslib_1.__importDefault)(require("./actions"));
const conditions_1 = (0, tslib_1.__importDefault)(require("./conditions"));
const sampleRate_1 = (0, tslib_1.__importDefault)(require("./sampleRate"));
const type_1 = (0, tslib_1.__importDefault)(require("./type"));
class Rule extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isMenuActionsOpen: false,
        };
        this.handleChangeMenuAction = () => {
            this.setState(state => ({
                isMenuActionsOpen: !state.isMenuActionsOpen,
            }));
        };
    }
    componentDidMount() {
        this.checkMenuActionsVisibility();
    }
    componentDidUpdate() {
        this.checkMenuActionsVisibility();
    }
    checkMenuActionsVisibility() {
        const { dragging, sorting } = this.props;
        const { isMenuActionsOpen } = this.state;
        if ((dragging || sorting) && isMenuActionsOpen) {
            this.setState({ isMenuActionsOpen: false });
        }
    }
    render() {
        const { rule, onEditRule, onDeleteRule, disabled, listeners, grabAttributes } = this.props;
        const { type, condition, sampleRate } = rule;
        const { isMenuActionsOpen } = this.state;
        return (<Columns>
        <GrabColumn>
          <tooltip_1.default title={disabled
                ? (0, locale_1.t)('You do not have permission to reorder dynamic sampling rules.')
                : undefined}>
            <IconGrabbableWrapper {...listeners} disabled={disabled} {...grabAttributes}>
              <iconGrabbable_1.IconGrabbable />
            </IconGrabbableWrapper>
          </tooltip_1.default>
        </GrabColumn>
        <Column>
          <type_1.default type={type}/>
        </Column>
        <Column>
          <conditions_1.default condition={condition}/>
        </Column>
        <CenteredColumn>
          <sampleRate_1.default sampleRate={sampleRate}/>
        </CenteredColumn>
        <Column>
          <actions_1.default onEditRule={onEditRule} onDeleteRule={onDeleteRule} disabled={disabled} onOpenMenuActions={this.handleChangeMenuAction} isMenuActionsOpen={isMenuActionsOpen}/>
        </Column>
      </Columns>);
    }
}
exports.default = Rule;
const Columns = (0, styled_1.default)('div') `
  display: grid;
  align-items: center;
  ${p => (0, utils_1.layout)(p.theme)}
  > * {
    overflow: visible;
    :nth-child(5n) {
      justify-content: flex-end;
    }
  }
`;
const Column = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(2)};
  cursor: default;
  white-space: pre-wrap;
  word-break: break-all;
`;
const GrabColumn = (0, styled_1.default)(Column) `
  cursor: inherit;
  [role='button'] {
    cursor: grab;
  }
`;
const CenteredColumn = (0, styled_1.default)(Column) `
  text-align: center;
  justify-content: center;
`;
const IconGrabbableWrapper = (0, styled_1.default)('div') `
  ${p => p.disabled &&
    `
    color: ${p.theme.disabled};
    cursor: not-allowed;
  `};
  outline: none;
`;
//# sourceMappingURL=index.jsx.map