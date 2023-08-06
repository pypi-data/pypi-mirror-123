Object.defineProperty(exports, "__esModule", { value: true });
const initializeOrg_1 = require("sentry-test/initializeOrg");
const theme_1 = require("app/utils/theme");
const utils_1 = require("app/views/releases/detail/utils");
describe('releases/detail/utils', () => {
    describe('generateReleaseMarkLines', () => {
        const { created, adopted, unadopted } = utils_1.releaseMarkLinesLabels;
        const { router } = (0, initializeOrg_1.initializeOrg)();
        // @ts-expect-error
        const release = TestStubs.Release();
        const project = release.projects[0];
        it('generates "Created" markline', () => {
            const marklines = (0, utils_1.generateReleaseMarkLines)(release, project, theme_1.lightTheme, router.location);
            expect(marklines.map(markline => markline.seriesName)).toEqual([created]);
        });
        it('generates also Adoption marklines if exactly one env is selected', () => {
            const marklines = (0, utils_1.generateReleaseMarkLines)(release, project, theme_1.lightTheme, Object.assign(Object.assign({}, router.location), { query: { environment: 'prod' } }));
            expect(marklines).toEqual([
                expect.objectContaining({
                    seriesName: created,
                    data: [
                        {
                            name: 1584925320000,
                            value: null,
                        },
                    ],
                }),
                expect.objectContaining({
                    seriesName: adopted,
                    data: [
                        {
                            name: 1585011750000,
                            value: null,
                        },
                    ],
                }),
                expect.objectContaining({
                    seriesName: unadopted,
                    data: [
                        {
                            name: 1585015350000,
                            value: null,
                        },
                    ],
                }),
            ]);
        });
        it('does not generate Adoption marklines for non-mobile projects', () => {
            const marklines = (0, utils_1.generateReleaseMarkLines)(Object.assign(Object.assign({}, release), { projects: [Object.assign(Object.assign({}, release.projects[0]), { platform: 'javascript' })] }), Object.assign(Object.assign({}, project), { platform: 'javascript' }), theme_1.lightTheme, Object.assign(Object.assign({}, router.location), { query: { environment: 'prod' } }));
            expect(marklines.map(markline => markline.seriesName)).toEqual([created]);
        });
        it('shows only marklines that are in current time window', () => {
            const marklines = (0, utils_1.generateReleaseMarkLines)(release, project, theme_1.lightTheme, Object.assign(Object.assign({}, router.location), { query: {
                    environment: 'prod',
                    pageStart: '2020-03-24T01:00:30Z',
                    pageEnd: '2020-03-24T01:03:30Z',
                } }));
            expect(marklines.map(markline => markline.seriesName)).toEqual([adopted]);
        });
    });
});
//# sourceMappingURL=utils.spec.jsx.map