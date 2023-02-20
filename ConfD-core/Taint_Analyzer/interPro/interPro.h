#include <bits/stdc++.h>
#include <queue>
#include <iostream>
#include <iterator>
#include "llvm/IR/GlobalVariable.h"
#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/IR/InstrTypes.h"
#include <string>
#include "llvm/IR/Value.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/Instruction.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Constants.h"
#include "llvm/Support/Casting.h"
#include "llvm/IR/User.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Operator.h"
#include "llvm/IR/Metadata.h"

using namespace std;
using namespace llvm;

namespace StaticAnalysis{
class TaintAnalysis{

public:
	static void mainfunctionProcess(Function& F, Instruction* line_no1);

	static void functionProcess(Function& F, Instruction* line_no1);

        static void visit(Instruction &I, Instruction* line_no1);

        static void taintStore(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void taintBinaryOperator(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void taintCallInst(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void Analysis(Function *func);

        static void propogateTaintToArguments(int taintedArgNo, Instruction &I, Function *F);

        static void taintLoad(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void taintIcmp(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void taintFcmp(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void taintGetElementPtr(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void taintSelect(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void taintConversion(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void taintBr(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void taintPhi(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1);

        static void printInst(std::queue<std::pair<Instruction *, Instruction *> > taintInst, Module& m);
	static void dataRange(Instruction * Inst, Module& m, raw_fd_ostream* stream);


};

}
