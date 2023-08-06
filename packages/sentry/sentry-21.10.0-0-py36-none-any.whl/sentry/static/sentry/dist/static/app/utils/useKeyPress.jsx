Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
/**
 * Hook to detect when a specific key is being pressed
 */
function useKeyPress(targetKey) {
    const [keyPressed, setKeyPressed] = (0, react_1.useState)(false);
    (0, react_1.useEffect)(() => {
        function downHandler({ key }) {
            if (key === targetKey) {
                setKeyPressed(true);
            }
        }
        function upHandler({ key }) {
            if (key === targetKey) {
                setKeyPressed(false);
            }
        }
        window.addEventListener('keydown', downHandler);
        window.addEventListener('keyup', upHandler);
        return () => {
            window.removeEventListener('keydown', downHandler);
            window.removeEventListener('keyup', upHandler);
        };
    }, [targetKey]);
    return keyPressed;
}
exports.default = useKeyPress;
//# sourceMappingURL=useKeyPress.jsx.map