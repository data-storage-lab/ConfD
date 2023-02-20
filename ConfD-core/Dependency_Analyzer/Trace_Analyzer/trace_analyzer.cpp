#include <fstream>
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
#include "llvm/Support/raw_ostream.h"
#include "llvm/Support/MemoryBuffer.h"
#include "clang/Basic/FileManager.h"
#include "llvm/IR/IRBuilder.h"
//#include "llvm/Support/CFG.h"

using namespace std;
using namespace llvm;

int numOfValue = 0;
std::error_code EC;
enum sys::fs::OpenFlags F_None;
std::string name = "critical";
StringRef filename(name);
llvm::raw_fd_ostream file(filename, EC, F_None);
int flag = 0; 
StringRef S;
namespace {
        struct TestPass : public ModulePass {

		string func_name = "PRS";
		static char ID;
		TestPass() : ModulePass(ID) {}

		virtual bool runOnModule(Module& m);
		BasicBlock& predecessorBB (BasicBlock& B);
	};


//Goes to the predecessor Basic Block to get the parameter involved in the Error	
BasicBlock& TestPass::predecessorBB (BasicBlock& B)
{
	flag = flag + 1;
	if (numOfValue < 2){
	for (BasicBlock* Pred : predecessors(&B))
        {
		BasicBlock& predecessor = *Pred;
		for (auto& i : predecessor){
       			unsigned opcode = i.getOpcode();
                        if (opcode == llvm::Instruction::ICmp)
                        {
				errs() << "found icmp instructions" << "\n";
				errs() << i << "\n";
                        	CmpInst* inst = dyn_cast<CmpInst>(&i);
                                Value* op1 = i.getOperand(0);
				Instruction* i1 = static_cast<Instruction*>(i.getOperand(0));
				unsigned opcode1 = i1->getOpcode();
				Value* op2 = i.getOperand(1);
				ConstantInt* ConI = dyn_cast<ConstantInt> (op2);
				//Instruction* i2 = static_cast<Instruction*>(i.getOperand(1));
				if ((ConI-> isZeroValue()) != 1){
					Instruction* i2 = static_cast<Instruction*>(i.getOperand(1));
				//unsigned opcode1 = i1->getOpcode();
				unsigned opcode2 = i2->getOpcode();
				errs() << opcode2 << "\n";
				//errs() << *i1 << ":" << *i2 << "\n";
				if (opcode1 == llvm::Instruction::Load && opcode2 == llvm::Instruction::Load){
					errs() << "found load instructions" << "\n";
					Value* op3 = i1->getOperand(0);
					Value* op4 = i2->getOperand(0);
				

				//Predicate code ICMP_UGT = 34; ICMP_SGT = 38
				if (inst->getPredicate() == 34 || inst->getPredicate() == 38){
					numOfValue = numOfValue + 2;
					errs() << "The correct state is :" << *op3 << " < " <<  *op4 << "\n";
					file << *op3 << " " << *op4 << " greater" << "\n"; 
				}

				//Predicate code ICMP_ULT = 36; ICMP_SLT = 40
				if (inst->getPredicate() == 36 || inst->getPredicate() == 40){
                                        numOfValue = numOfValue + 2;
                                        errs() << "The correct state is :" << *op3 << " > " <<  *op4 << "\n";
					file << *op3 << " " << *op4 << " lesser" << "\n";
                                }
				}
				else
				{
					Value* op3 = i1->getOperand(1);
					Value* op4 = i2->getOperand(1);
					Instruction* i3 = static_cast<Instruction*>(i1->getOperand(1));
					Instruction* i4 = static_cast<Instruction*>(i2->getOperand(1));
					unsigned opcode3 = i3->getOpcode();
					unsigned opcode4 = i4->getOpcode();
					//errs() << *i3 << ":" << *i4 << "\n";
					if (opcode3 == llvm::Instruction::Load && opcode4 == llvm::Instruction::Load){
						errs() << "found load instructions" << "\n";
						//Predicate code ICMP_UGT = 34; ICMP_SGT = 38
						if (inst->getPredicate() == 34 || inst->getPredicate() == 38){
							numOfValue = numOfValue + 2;
							errs() << "The correct state is :" << *op3 << " > " <<  *op4 << "\n";
							file << *op3 << " " << *op4 << " greater" << "\n";
						}

						//Predicate code ICMP_ULT = 36; ICMP_SLT = 40
						if (inst->getPredicate() == 36 || inst->getPredicate() == 40){
							numOfValue = numOfValue + 2;
							errs() << "The correct state is :" << *op3 << " < " <<  *op4 << "\n";
							file << *op3 << " " << *op4 << " lesser" << "\n";
						}
					}
					else if (opcode3 == llvm::Instruction::Load && opcode4 != llvm::Instruction::Load){
							Value* op5 = i4->getOperand(1);
							Instruction* i5 = static_cast<Instruction*>(i4->getOperand(1));
							if (inst->getPredicate() == 34 || inst->getPredicate() == 38){
								numOfValue = numOfValue + 2;
								errs() << "The correct state is :" << *op3 << " >" <<  *op5 << "\n";
								file << *op3 << " " << *op5 << " greater" << "\n";
							}

							//Predicate code ICMP_ULT = 36; ICMP_SLT = 4
							if (inst->getPredicate() == 36 || inst->getPredicate() == 40){
								numOfValue = numOfValue + 2;
								errs() << "The correct state is :" << *op3 << " < " <<  *op5 << "\n";
								file << *op3 << " " << *op5 << " lesser" << "\n";
							}
						}
					
				}
				}
			//}

				//if (opcode1 == llvm::Instruction::Call || opcode2 == llvm::Instruction::Call){
				if (opcode1 == llvm::Instruction::Call) {
					errs() << "found call instructions" << "\n";

                                //CallInst* inst1 = cast<CallInst>(i.getOperand(0));
                                //Function* func = inst1->getCalledFunction();
				CallInst* i3 = cast<CallInst>(i.getOperand(0));
				//CallInst* i4 = cast<CallInst>(i.getOperand(1));
				Function* func1 = i3->getCalledFunction();
				//Function* func2 = i4->getCalledFunction();
                                StringRef S1 = func1->getName();
				//StringRef S2 = func2->getName();

                                //Predicate code ICMP_EQ = 32
                                if (inst->getPredicate() == 32)
                                {
                                	numOfValue = numOfValue + 1;
                                        errs() << numOfValue << "\n";
                                        errs() << "The correct state is : !" <<  S1 << "\n";
					if (flag ==2)
						file << S << " " << S1 << " disable" << "\n";
					else
						file << "variable" << " " << S1 << " disable" << "\n";
                                }

                                //Predicate code  ICMP_NE = 33
                                if (inst->getPredicate() == 33)
                                {
                                	numOfValue = numOfValue + 1;
                                        errs() << numOfValue << "\n";
                                        errs() << "The correct state is : " <<  S1 << "\n";
					if (flag ==2)
						file << S << " " << S1 << " enable" << "\n";
					else
						file << "variable" << " " << S1 << " enable" << "\n";
                                }
				if (flag == 1)
					S = S1;
			}
		}
		}
		return predecessor;
	}
	}
}


bool TestPass::runOnModule(Module& m) {
	//Gets the common line (contains error) between two parameters from a file
	char *Filename = "resize_inodesparse_super";
	std::ifstream infile(Filename);
	std::string line;
	std::getline(infile, line);
	//errs() << "after getline: " << line << "\n";
	const char* string2 = line.c_str();
	//errs() << string2 << "\n";


	
        for(auto& F : m){
                //if (F.getName() == func_name ){
                  //      errs() << "Hello from: "<< F.getName() << "\n";
                        for (auto& B : F) {
                                for (auto& I : B) {
					//errs() << I << "\n";
					std::string str;

					llvm::raw_string_ostream ss(str);
					ss << I;
					const char* string1 = ss.str().c_str();

					//Searches for the common error line in each instruction
					if (strcmp (string1, string2) == 0) 
					{
						errs() << "it's a match" << "\n";
						//When the instruction is found, goes to predecessor Basic Block to find the involved parameter
						BasicBlock& B1 = predecessorBB (B);
						errs() << numOfValue << "\n";
						if (numOfValue < 2){
						//Goes to predecessor Basic Block of the predecessor Basic Block to find another involved parameter
						BasicBlock& B2 = predecessorBB (B1);
						}
					}
				}
			}
		//}
	}
	return false;
	
	}
}

//Registers the pass as 'test', the library name is 'libTestPass.so'
char TestPass::ID = 0;
static RegisterPass<TestPass> SCCReg("test", "Test Pass");
