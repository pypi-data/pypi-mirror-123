Object.defineProperty(exports, "__esModule", { value: true });
/* global process */
require("@visual-snapshot/jest");
process.on('unhandledRejection', reason => {
    // eslint-disable-next-line no-console
    console.error(reason);
});
//# sourceMappingURL=setupFramework.js.map