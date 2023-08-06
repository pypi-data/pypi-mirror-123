Object.defineProperty(exports, "__esModule", { value: true });
exports.Divider = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const events_1 = require("app/utils/events");
function EventTitleTreeLabel({ treeLabel }) {
    const firstFourParts = treeLabel.slice(0, 4);
    const remainingParts = treeLabel.slice(firstFourParts.length);
    return (<Wrapper>
      <FirstFourParts>
        {firstFourParts.map((part, index) => {
            const label = (0, events_1.getTreeLabelPartDetails)(part);
            if (index !== firstFourParts.length - 1) {
                return (<react_1.Fragment key={index}>
                <PriorityLabel>{label}</PriorityLabel>
                <exports.Divider>{'|'}</exports.Divider>
              </react_1.Fragment>);
            }
            return <PriorityLabel key={index}>{label}</PriorityLabel>;
        })}
      </FirstFourParts>
      {!!remainingParts.length && (<RemainingLabels>
          {remainingParts.map((part, index) => {
                const label = (0, events_1.getTreeLabelPartDetails)(part);
                return (<react_1.Fragment key={index}>
                <exports.Divider>{'|'}</exports.Divider>
                <Label>{label}</Label>
              </react_1.Fragment>);
            })}
        </RemainingLabels>)}
    </Wrapper>);
}
exports.default = EventTitleTreeLabel;
const Wrapper = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-template-columns: auto 1fr;
  align-items: center;
`;
const FirstFourParts = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-auto-flow: column;
  align-items: center;
`;
const Label = (0, styled_1.default)('div') `
  display: inline-block;
`;
const PriorityLabel = (0, styled_1.default)(Label) `
  ${overflowEllipsis_1.default}
  display: inline-block;
`;
const RemainingLabels = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}
  display: inline-block;
  min-width: 50px;
`;
exports.Divider = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray200};
  display: inline-block;
  padding: 0 ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=eventTitleTreeLabel.jsx.map