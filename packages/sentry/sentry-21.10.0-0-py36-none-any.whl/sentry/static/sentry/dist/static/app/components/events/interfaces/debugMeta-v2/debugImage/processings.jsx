Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const item_1 = (0, tslib_1.__importDefault)(require("../processing/item"));
const list_1 = (0, tslib_1.__importDefault)(require("../processing/list"));
const processingIcon_1 = (0, tslib_1.__importDefault)(require("./processingIcon"));
function Processings({ unwind_status, debug_status }) {
    const items = [];
    if (debug_status) {
        items.push(<StyledProcessingItem key="symbolication" type="symbolication" icon={<processingIcon_1.default status={debug_status}/>}/>);
    }
    if (unwind_status) {
        items.push(<StyledProcessingItem key="stack_unwinding" type="stack_unwinding" icon={<processingIcon_1.default status={unwind_status}/>}/>);
    }
    return <StyledProcessingList items={items}/>;
}
exports.default = Processings;
const StyledProcessingList = (0, styled_1.default)(list_1.default) `
  display: flex;
  flex-wrap: wrap;
  margin-bottom: -${(0, space_1.default)(1)};
`;
const StyledProcessingItem = (0, styled_1.default)(item_1.default) `
  :not(:last-child) {
    padding-right: ${(0, space_1.default)(2)};
  }
  padding-bottom: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=processings.jsx.map