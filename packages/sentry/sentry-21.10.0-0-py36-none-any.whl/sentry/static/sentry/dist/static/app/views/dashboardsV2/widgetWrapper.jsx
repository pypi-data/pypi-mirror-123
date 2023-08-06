Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const WidgetWrapper = (0, styled_1.default)(framer_motion_1.motion.div) `
  position: relative;
  touch-action: manipulation;

  ${p => {
    switch (p.displayType) {
        case 'big_number':
            return `
          /* 2 cols */
          grid-area: span 1 / span 2;

          @media (min-width: ${p.theme.breakpoints[0]}) {
            /* 4 cols */
            grid-area: span 1 / span 1;
          }

          @media (min-width: ${p.theme.breakpoints[3]}) {
            /* 6 and 8 cols */
            grid-area: span 1 / span 2;
          }
        `;
        default:
            return `
          /* 2, 4, 6 and 8 cols */
          grid-area: span 2 / span 2;
        `;
    }
}};
`;
exports.default = WidgetWrapper;
//# sourceMappingURL=widgetWrapper.jsx.map