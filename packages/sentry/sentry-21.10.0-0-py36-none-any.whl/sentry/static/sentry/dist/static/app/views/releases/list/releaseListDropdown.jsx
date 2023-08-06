Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const ReleaseListDropdown = ({ label: prefix, options, selected, onSelect, className, }) => {
    var _a;
    const optionEntries = Object.entries(options);
    const selectedLabel = (_a = optionEntries.find(([key, _value]) => key === selected)) === null || _a === void 0 ? void 0 : _a[1];
    return (<dropdownControl_1.default alwaysRenderMenu={false} buttonProps={{ prefix }} label={selectedLabel === null || selectedLabel === void 0 ? void 0 : selectedLabel.label} className={className}>
      {optionEntries.map((_a) => {
            var [key, _b] = _a, { label, tooltip } = _b, props = (0, tslib_1.__rest)(_b, ["label", "tooltip"]);
            return (<tooltip_1.default key={key} containerDisplayMode="block" title={tooltip} delay={500} disabled={!tooltip}>
          <dropdownControl_1.DropdownItem onSelect={onSelect} eventKey={key} isActive={selected === key} {...props}>
            {label}
          </dropdownControl_1.DropdownItem>
        </tooltip_1.default>);
        })}
    </dropdownControl_1.default>);
};
exports.default = ReleaseListDropdown;
//# sourceMappingURL=releaseListDropdown.jsx.map