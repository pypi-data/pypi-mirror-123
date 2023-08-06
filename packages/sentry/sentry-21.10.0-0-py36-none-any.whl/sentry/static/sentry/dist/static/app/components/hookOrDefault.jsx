Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
/**
 * Use this instead of the usual ternery operator when using getsentry hooks.
 * So in lieu of:
 *
 *  HookStore.get('component:org-auth-view').length
 *   ? HookStore.get('component:org-auth-view')[0]()
 *   : OrganizationAuth
 *
 * do this instead:
 *
 *   const HookedOrganizationAuth = HookOrDefault({
 *     hookName:'component:org-auth-view',
 *     defaultComponent: OrganizationAuth,
 *   })
 *
 * Note, you will need to add the hookstore function in getsentry [0] first and
 * then register the types [2] and validHookName [1] in sentry.
 *
 * [0] /getsentry/static/getsentry/gsApp/registerHooks.jsx
 * [1] /sentry/app/stores/hookStore.tsx
 * [2] /sentry/app/types/hooks.ts
 */
function HookOrDefault({ hookName, defaultComponent, defaultComponentPromise, }) {
    class HookOrDefaultComponent extends React.Component {
        constructor() {
            super(...arguments);
            this.state = {
                hooks: hookStore_1.default.get(hookName),
            };
            this.unlistener = hookStore_1.default.listen((name, hooks) => name === hookName && this.setState({ hooks }), undefined);
        }
        componentWillUnmount() {
            var _a;
            (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
        }
        get defaultComponent() {
            // If `defaultComponentPromise` is passed, then return a Suspended component
            if (defaultComponentPromise) {
                const Component = React.lazy(defaultComponentPromise);
                return (props) => (<React.Suspense fallback={null}>
            <Component {...props}/>
          </React.Suspense>);
            }
            return defaultComponent;
        }
        render() {
            var _a, _b;
            const hookExists = this.state.hooks && this.state.hooks.length;
            const componentFromHook = (_b = (_a = this.state.hooks)[0]) === null || _b === void 0 ? void 0 : _b.call(_a);
            const HookComponent = hookExists && componentFromHook ? componentFromHook : this.defaultComponent;
            return HookComponent ? <HookComponent {...this.props}/> : null;
        }
    }
    HookOrDefaultComponent.displayName = `HookOrDefaultComponent(${hookName})`;
    return HookOrDefaultComponent;
}
exports.default = HookOrDefault;
//# sourceMappingURL=hookOrDefault.jsx.map