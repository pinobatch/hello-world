If you get a `.macpack` error when building a cc65 or ca65 project,
check your include path. ca65 processes `.macpack` thus:

1. `DoMacPack()` in pseudo.c calls `NewInputFile(SB_GetConstBuf(&CurTok.SVal))`
2. `NewInputFile()` in scanner.c calls `SearchFile(IncSearchPath, Name)`

According to <https://cc65.github.io/doc/ca65.html#s3> and incpath.c,
the relevant paths in `IncSearchPath` are

1. The current file's directory
2. Directories added with `-I`
3. Directories added by `FinishIncludePaths()` in incpath.c

The `FinishIncludePaths()` directories are as follows:

1. `$CA65_INC`
2. `$CC65_HOME/asminc`
3. On non-Windows, the directory passed to `-DCA65_INC=` when ca65 was compiled
4. On Windows only, `directory_containing_exe\..\asminc`

