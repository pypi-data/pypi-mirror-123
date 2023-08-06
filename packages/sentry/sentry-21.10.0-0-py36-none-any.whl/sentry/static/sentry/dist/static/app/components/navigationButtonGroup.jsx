Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const NavigationButtonGroup = ({ links, hasNext = false, hasPrevious = false, className, size, onOldestClick, onOlderClick, onNewerClick, onNewestClick, }) => (<buttonBar_1.default className={className} merged>
    <button_1.default size={size} to={links[0]} disabled={!hasPrevious} label={(0, locale_1.t)('Oldest')} icon={<icons_1.IconPrevious size="xs"/>} onClick={onOldestClick}/>
    <button_1.default size={size} to={links[1]} disabled={!hasPrevious} onClick={onOlderClick}>
      {(0, locale_1.t)('Older')}
    </button_1.default>
    <button_1.default size={size} to={links[2]} disabled={!hasNext} onClick={onNewerClick}>
      {(0, locale_1.t)('Newer')}
    </button_1.default>
    <button_1.default size={size} to={links[3]} disabled={!hasNext} label={(0, locale_1.t)('Newest')} icon={<icons_1.IconNext size="xs"/>} onClick={onNewestClick}/>
  </buttonBar_1.default>);
exports.default = NavigationButtonGroup;
//# sourceMappingURL=navigationButtonGroup.jsx.map