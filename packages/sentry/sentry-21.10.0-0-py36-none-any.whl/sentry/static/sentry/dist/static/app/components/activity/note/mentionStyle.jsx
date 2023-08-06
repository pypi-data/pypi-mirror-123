Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
/**
 * Note this is an object for `react-mentions` component and
 * not a styled component/emotion style
 */
function mentionStyle({ theme, minHeight }) {
    return {
        control: {
            backgroundColor: `${theme.background}`,
            fontSize: 15,
            fontWeight: 'normal',
        },
        input: {
            margin: 0,
        },
        '&singleLine': {
            control: {
                display: 'inline-block',
                width: 130,
            },
            highlighter: {
                padding: 1,
                border: '2px inset transparent',
            },
            input: {
                padding: 1,
                border: '2px inset',
            },
        },
        '&multiLine': {
            control: {
                fontFamily: 'Rubik, Avenir Next, Helvetica Neue, sans-serif',
                minHeight,
            },
            highlighter: {
                padding: 20,
                minHeight,
            },
            input: {
                padding: `${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)} 0`,
                minHeight,
                overflow: 'auto',
                outline: 0,
                border: 0,
            },
        },
        suggestions: {
            list: {
                maxHeight: 150,
                overflow: 'auto',
                backgroundColor: `${theme.background}`,
                border: '1px solid rgba(0,0,0,0.15)',
                fontSize: 12,
            },
            item: {
                padding: '5px 15px',
                borderBottom: '1px solid rgba(0,0,0,0.15)',
                '&focused': {
                    backgroundColor: `${theme.backgroundSecondary}`,
                },
            },
        },
    };
}
exports.default = mentionStyle;
//# sourceMappingURL=mentionStyle.jsx.map