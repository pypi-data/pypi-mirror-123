Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/avatar/styles");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const COLORS = [
    '#4674ca',
    '#315cac',
    '#57be8c',
    '#3fa372',
    '#f9a66d',
    '#ec5e44',
    '#e63717',
    '#f868bc',
    '#6c5fc7',
    '#4e3fb4',
    '#57b1be',
    '#847a8c', // gray
];
function hashIdentifier(identifier) {
    identifier += '';
    let hash = 0;
    for (let i = 0; i < identifier.length; i++) {
        hash += identifier.charCodeAt(i);
    }
    return hash;
}
function getColor(identifier) {
    // Gray if the identifier is not set
    if (identifier === undefined) {
        return '#847a8c';
    }
    const id = hashIdentifier(identifier);
    return COLORS[id % COLORS.length];
}
function getInitials(displayName) {
    const names = ((typeof displayName === 'string' && displayName.trim()) || '?').split(' ');
    // Use Array.from as slicing and substring() work on ucs2 segments which
    // results in only getting half of any 4+ byte character.
    let initials = Array.from(names[0])[0];
    if (names.length > 1) {
        initials += Array.from(names[names.length - 1])[0];
    }
    return initials.toUpperCase();
}
/**
 * Also see avatar.py. Anything changed in this file (how colors are selected,
 * the svg, etc) will also need to be changed there.
 */
const LetterAvatar = (0, styled_1.default)((_a) => {
    var { identifier, displayName, round: _round, forwardedRef, suggested } = _a, props = (0, tslib_1.__rest)(_a, ["identifier", "displayName", "round", "forwardedRef", "suggested"]);
    return (<svg ref={forwardedRef} viewBox="0 0 120 120" {...props}>
      <rect x="0" y="0" width="120" height="120" rx="15" ry="15" fill={suggested ? '#FFFFFF' : getColor(identifier)}/>
      <text x="50%" y="50%" fontSize="65" style={{ dominantBaseline: 'central' }} textAnchor="middle" fill={suggested ? theme_1.default.gray400 : '#FFFFFF'}>
        {getInitials(displayName)}
      </text>
    </svg>);
}) `
  ${styles_1.imageStyle};
`;
LetterAvatar.defaultProps = {
    round: false,
};
exports.default = React.forwardRef((props, ref) => (<LetterAvatar forwardedRef={ref} {...props}/>));
//# sourceMappingURL=letterAvatar.jsx.map