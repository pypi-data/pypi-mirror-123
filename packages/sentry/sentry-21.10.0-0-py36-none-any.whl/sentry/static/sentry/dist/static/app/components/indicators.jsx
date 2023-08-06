Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const indicator_1 = require("app/actionCreators/indicator");
const toastIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/alerts/toastIndicator"));
const indicatorStore_1 = (0, tslib_1.__importDefault)(require("app/stores/indicatorStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
const Toasts = (0, styled_1.default)('div') `
  position: fixed;
  right: 30px;
  bottom: 30px;
  z-index: ${p => p.theme.zIndex.toast};
`;
function Indicators(props) {
    const items = (0, useLegacyStore_1.useLegacyStore)(indicatorStore_1.default);
    return (<Toasts {...props}>
      <framer_motion_1.AnimatePresence>
        {items.map((indicator, i) => (
        // We purposefully use `i` as key here because of transitions
        // Toasts can now queue up, so when we change from [firstToast] -> [secondToast],
        // we don't want to  animate `firstToast` out and `secondToast` in, rather we want
        // to replace `firstToast` with `secondToast`
        <toastIndicator_1.default onDismiss={indicator_1.removeIndicator} indicator={indicator} key={i}/>))}
      </framer_motion_1.AnimatePresence>
    </Toasts>);
}
exports.default = Indicators;
//# sourceMappingURL=indicators.jsx.map