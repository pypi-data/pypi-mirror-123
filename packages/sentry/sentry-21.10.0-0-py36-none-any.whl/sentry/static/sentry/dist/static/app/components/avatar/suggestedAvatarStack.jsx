Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const actorAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/actorAvatar"));
const baseAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/baseAvatar"));
// Constrain the number of visible suggestions
const MAX_SUGGESTIONS = 5;
const SuggestedAvatarStack = (_a) => {
    var { owners, tooltip, tooltipOptions } = _a, props = (0, tslib_1.__rest)(_a, ["owners", "tooltip", "tooltipOptions"]);
    const backgroundAvatarProps = Object.assign(Object.assign({}, props), { round: owners[0].type === 'user', suggested: true });
    const numAvatars = Math.min(owners.length, MAX_SUGGESTIONS);
    return (<AvatarStack>
      {[...Array(numAvatars - 1)].map((_, i) => (<BackgroundAvatar {...backgroundAvatarProps} key={i} type="background" index={i} hasTooltip={false}/>))}
      <Avatar {...props} suggested actor={owners[0]} index={numAvatars - 1} tooltip={tooltip} tooltipOptions={Object.assign(Object.assign({}, tooltipOptions), { skipWrapper: true })}/>
    </AvatarStack>);
};
const AvatarStack = (0, styled_1.default)('div') `
  display: flex;
  align-content: center;
  flex-direction: row-reverse;
`;
const translateStyles = (props) => (0, react_1.css) `
  transform: translateX(${60 * props.index}%);
`;
const Avatar = (0, styled_1.default)(actorAvatar_1.default) `
  ${translateStyles}
`;
const BackgroundAvatar = (0, styled_1.default)(baseAvatar_1.default) `
  ${translateStyles}
`;
exports.default = SuggestedAvatarStack;
//# sourceMappingURL=suggestedAvatarStack.jsx.map