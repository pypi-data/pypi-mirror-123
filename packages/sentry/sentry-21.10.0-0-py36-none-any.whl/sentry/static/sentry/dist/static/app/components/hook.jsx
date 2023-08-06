Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
/**
 * Instead of accessing the HookStore directly, use this.
 *
 * If the hook slot needs to perform anything w/ the hooks, you can pass a
 * function as a child and you will receive an object with a `hooks` key
 *
 * Example:
 *
 *   <Hook name="my-hook">
 *     {({hooks}) => hooks.map(hook => (
 *       <Wrapper>{hook}</Wrapper>
 *     ))}
 *   </Hook>
 */
function Hook(_a) {
    var { name } = _a, props = (0, tslib_1.__rest)(_a, ["name"]);
    class HookComponent extends React.Component {
        constructor() {
            super(...arguments);
            this.state = {
                hooks: hookStore_1.default.get(name).map(cb => cb(props)),
            };
            this.unsubscribe = hookStore_1.default.listen((hookName, hooks) => this.handleHooks(hookName, hooks), undefined);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        handleHooks(hookName, hooks) {
            // Make sure that the incoming hook update matches this component's hook name
            if (hookName !== name) {
                return;
            }
            this.setState({ hooks: hooks.map(cb => cb(props)) });
        }
        render() {
            const { children } = props;
            if (!this.state.hooks || !this.state.hooks.length) {
                return null;
            }
            if (typeof children === 'function') {
                return children({ hooks: this.state.hooks });
            }
            return this.state.hooks;
        }
    }
    HookComponent.displayName = `Hook(${name})`;
    return <HookComponent />;
}
exports.default = Hook;
//# sourceMappingURL=hook.jsx.map