Object.defineProperty(exports, "__esModule", { value: true });
exports.getSortedRegisters = void 0;
const registers_1 = require("./registers");
function getRegisterMap(deviceArch) {
    if (deviceArch.startsWith('x86_64')) {
        return registers_1.REGISTERS_X86_64;
    }
    if (deviceArch.startsWith('x86')) {
        return registers_1.REGISTERS_X86;
    }
    if (deviceArch.startsWith('arm64')) {
        return registers_1.REGISTERS_ARM64;
    }
    if (deviceArch.startsWith('arm')) {
        return registers_1.REGISTERS_ARM64;
    }
    if (deviceArch.startsWith('mips')) {
        return registers_1.REGISTERS_MIPS;
    }
    if (deviceArch.startsWith('ppc')) {
        return registers_1.REGISTERS_PPC;
    }
    return undefined;
}
function getRegisterIndex(register, registerMap) {
    var _a;
    return (_a = registerMap[register[0] === '$' ? register.slice(1) : register]) !== null && _a !== void 0 ? _a : -1;
}
function getSortedRegisters(registers, deviceArch) {
    const entries = Object.entries(registers);
    if (!deviceArch) {
        return entries;
    }
    const registerMap = getRegisterMap(deviceArch);
    if (!registerMap) {
        return entries;
    }
    return entries.sort((a, b) => getRegisterIndex(a[0], registerMap) - getRegisterIndex(b[0], registerMap));
}
exports.getSortedRegisters = getSortedRegisters;
//# sourceMappingURL=utils.jsx.map