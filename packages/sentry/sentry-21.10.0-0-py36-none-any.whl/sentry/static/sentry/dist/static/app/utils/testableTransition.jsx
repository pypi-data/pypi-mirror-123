Object.defineProperty(exports, "__esModule", { value: true });
const constants_1 = require("app/constants");
/**
 * Use with a framer-motion transition to disable the animation in testing
 * environments.
 *
 * If your animation has no transition you can simply specify
 *
 * ```tsx
 * Component.defaultProps = {
 *   transition: testableTransition(),
 * }
 * ```
 *
 * This function simply disables the animation `type`.
 */
const testableTransition = !constants_1.IS_ACCEPTANCE_TEST
    ? (t) => t
    : function () {
        return {
            delay: 0,
            staggerChildren: 0,
            type: false,
        };
    };
exports.default = testableTransition;
//# sourceMappingURL=testableTransition.jsx.map