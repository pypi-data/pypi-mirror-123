Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const panels_1 = require("app/components/panels");
const toolbarHeader_1 = (0, tslib_1.__importDefault)(require("app/components/toolbarHeader"));
const locale_1 = require("app/locale");
const groupingStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupingStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const initialState = {
    mergeCount: 0,
};
class SimilarToolbar extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = initialState;
        this.onGroupChange = ({ mergeList }) => {
            if (!(mergeList === null || mergeList === void 0 ? void 0 : mergeList.length)) {
                return;
            }
            if (mergeList.length !== this.state.mergeCount) {
                this.setState({ mergeCount: mergeList.length });
            }
        };
        this.listener = groupingStore_1.default.listen(this.onGroupChange, undefined);
    }
    componentWillUnmount() {
        (0, callIfFunction_1.callIfFunction)(this.listener);
    }
    render() {
        const { onMerge, v2 } = this.props;
        const { mergeCount } = this.state;
        return (<panels_1.PanelHeader hasButtons>
        <confirm_1.default data-test-id="merge" disabled={mergeCount === 0} message={(0, locale_1.t)('Are you sure you want to merge these issues?')} onConfirm={onMerge}>
          <button_1.default size="small" title={(0, locale_1.t)('Merging %s issues', mergeCount)}>
            {(0, locale_1.t)('Merge %s', `(${mergeCount || 0})`)}
          </button_1.default>
        </confirm_1.default>

        <Columns>
          <StyledToolbarHeader>{(0, locale_1.t)('Events')}</StyledToolbarHeader>

          {v2 ? (<StyledToolbarHeader>{(0, locale_1.t)('Score')}</StyledToolbarHeader>) : (<react_1.Fragment>
              <StyledToolbarHeader>{(0, locale_1.t)('Exception')}</StyledToolbarHeader>
              <StyledToolbarHeader>{(0, locale_1.t)('Message')}</StyledToolbarHeader>
            </react_1.Fragment>)}
        </Columns>
      </panels_1.PanelHeader>);
    }
}
exports.default = SimilarToolbar;
const Columns = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  flex-shrink: 0;
  min-width: 300px;
  width: 300px;
`;
const StyledToolbarHeader = (0, styled_1.default)(toolbarHeader_1.default) `
  flex: 1;
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  padding: ${(0, space_1.default)(0.5)} 0;
`;
//# sourceMappingURL=toolbar.jsx.map