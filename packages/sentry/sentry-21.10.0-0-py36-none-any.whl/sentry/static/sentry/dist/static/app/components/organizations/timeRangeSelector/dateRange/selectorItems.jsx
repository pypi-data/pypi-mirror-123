Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const relativeSelector_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/timeRangeSelector/dateRange/relativeSelector"));
const selectorItem_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/timeRangeSelector/dateRange/selectorItem"));
const locale_1 = require("app/locale");
const SelectorItems = ({ shouldShowRelative, shouldShowAbsolute, handleSelectRelative, handleAbsoluteClick, relativeSelected, relativePeriods, isAbsoluteSelected, }) => (<React.Fragment>
    {shouldShowRelative && (<relativeSelector_1.default onClick={handleSelectRelative} selected={relativeSelected} relativePeriods={relativePeriods}/>)}
    {shouldShowAbsolute && (<selectorItem_1.default onClick={handleAbsoluteClick} value="absolute" label={(0, locale_1.t)('Absolute date')} selected={isAbsoluteSelected} last/>)}
  </React.Fragment>);
exports.default = SelectorItems;
//# sourceMappingURL=selectorItems.jsx.map