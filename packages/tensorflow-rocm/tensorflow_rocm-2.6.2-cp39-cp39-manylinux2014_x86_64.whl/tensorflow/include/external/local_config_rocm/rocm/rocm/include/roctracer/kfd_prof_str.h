// automatically generated

/*
Copyright (c) 2018 Advanced Micro Devices, Inc. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

/////////////////////////////////////////////////////////////////////////////

#ifndef INC_KFD_PROF_STR_H_
#define INC_KFD_PROF_STR_H_

#include <dlfcn.h>
#include <string.h>
#include <roctracer_kfd.h>
#include <hsakmt.h>
#define PUBLIC_API __attribute__((visibility("default")))

// section: API ID enumeration

enum kfd_api_id_t {
  // block: HSAKMTAPI API
  KFD_API_ID_hsaKmtOpenKFD = 0,
  KFD_API_ID_hsaKmtCloseKFD = 1,
  KFD_API_ID_hsaKmtGetVersion = 2,
  KFD_API_ID_hsaKmtAcquireSystemProperties = 3,
  KFD_API_ID_hsaKmtReleaseSystemProperties = 4,
  KFD_API_ID_hsaKmtGetNodeProperties = 5,
  KFD_API_ID_hsaKmtGetNodeMemoryProperties = 6,
  KFD_API_ID_hsaKmtGetNodeCacheProperties = 7,
  KFD_API_ID_hsaKmtGetNodeIoLinkProperties = 8,
  KFD_API_ID_hsaKmtCreateEvent = 9,
  KFD_API_ID_hsaKmtDestroyEvent = 10,
  KFD_API_ID_hsaKmtSetEvent = 11,
  KFD_API_ID_hsaKmtResetEvent = 12,
  KFD_API_ID_hsaKmtQueryEventState = 13,
  KFD_API_ID_hsaKmtWaitOnEvent = 14,
  KFD_API_ID_hsaKmtWaitOnMultipleEvents = 15,
  KFD_API_ID_hsaKmtReportQueue = 16,
  KFD_API_ID_hsaKmtCreateQueue = 17,
  KFD_API_ID_hsaKmtUpdateQueue = 18,
  KFD_API_ID_hsaKmtDestroyQueue = 19,
  KFD_API_ID_hsaKmtSetQueueCUMask = 20,
  KFD_API_ID_hsaKmtGetQueueInfo = 21,
  KFD_API_ID_hsaKmtSetMemoryPolicy = 22,
  KFD_API_ID_hsaKmtAllocMemory = 23,
  KFD_API_ID_hsaKmtFreeMemory = 24,
  KFD_API_ID_hsaKmtRegisterMemory = 25,
  KFD_API_ID_hsaKmtRegisterMemoryToNodes = 26,
  KFD_API_ID_hsaKmtRegisterMemoryWithFlags = 27,
  KFD_API_ID_hsaKmtRegisterGraphicsHandleToNodes = 28,
  KFD_API_ID_hsaKmtShareMemory = 29,
  KFD_API_ID_hsaKmtRegisterSharedHandle = 30,
  KFD_API_ID_hsaKmtRegisterSharedHandleToNodes = 31,
  KFD_API_ID_hsaKmtProcessVMRead = 32,
  KFD_API_ID_hsaKmtProcessVMWrite = 33,
  KFD_API_ID_hsaKmtDeregisterMemory = 34,
  KFD_API_ID_hsaKmtMapMemoryToGPU = 35,
  KFD_API_ID_hsaKmtMapMemoryToGPUNodes = 36,
  KFD_API_ID_hsaKmtUnmapMemoryToGPU = 37,
  KFD_API_ID_hsaKmtMapGraphicHandle = 38,
  KFD_API_ID_hsaKmtUnmapGraphicHandle = 39,
  KFD_API_ID_hsaKmtAllocQueueGWS = 40,
  KFD_API_ID_hsaKmtDbgRegister = 41,
  KFD_API_ID_hsaKmtDbgUnregister = 42,
  KFD_API_ID_hsaKmtDbgWavefrontControl = 43,
  KFD_API_ID_hsaKmtDbgAddressWatch = 44,
  KFD_API_ID_hsaKmtQueueSuspend = 45,
  KFD_API_ID_hsaKmtQueueResume = 46,
  KFD_API_ID_hsaKmtEnableDebugTrap = 47,
  KFD_API_ID_hsaKmtEnableDebugTrapWithPollFd = 48,
  KFD_API_ID_hsaKmtDisableDebugTrap = 49,
  KFD_API_ID_hsaKmtQueryDebugEvent = 50,
  KFD_API_ID_hsaKmtGetQueueSnapshot = 51,
  KFD_API_ID_hsaKmtSendHostTrap = 52,
  KFD_API_ID_hsaKmtSetWaveLaunchTrapOverride = 53,
  KFD_API_ID_hsaKmtSetWaveLaunchMode = 54,
  KFD_API_ID_hsaKmtGetKernelDebugTrapVersionInfo = 55,
  KFD_API_ID_hsaKmtGetThunkDebugTrapVersionInfo = 56,
  KFD_API_ID_hsaKmtSetAddressWatch = 57,
  KFD_API_ID_hsaKmtClearAddressWatch = 58,
  KFD_API_ID_hsaKmtEnablePreciseMemoryOperations = 59,
  KFD_API_ID_hsaKmtDisablePreciseMemoryOperations = 60,
  KFD_API_ID_hsaKmtGetClockCounters = 61,
  KFD_API_ID_hsaKmtPmcGetCounterProperties = 62,
  KFD_API_ID_hsaKmtPmcRegisterTrace = 63,
  KFD_API_ID_hsaKmtPmcUnregisterTrace = 64,
  KFD_API_ID_hsaKmtPmcAcquireTraceAccess = 65,
  KFD_API_ID_hsaKmtPmcReleaseTraceAccess = 66,
  KFD_API_ID_hsaKmtPmcStartTrace = 67,
  KFD_API_ID_hsaKmtPmcQueryTrace = 68,
  KFD_API_ID_hsaKmtPmcStopTrace = 69,
  KFD_API_ID_hsaKmtSetTrapHandler = 70,
  KFD_API_ID_hsaKmtGetTileConfig = 71,
  KFD_API_ID_hsaKmtQueryPointerInfo = 72,
  KFD_API_ID_hsaKmtSetMemoryUserData = 73,
  KFD_API_ID_hsaKmtSPMAcquire = 74,
  KFD_API_ID_hsaKmtSPMRelease = 75,
  KFD_API_ID_hsaKmtSPMSetDestBuffer = 76,
  KFD_API_ID_hsaKmtSVMSetAttr = 77,
  KFD_API_ID_hsaKmtSVMGetAttr = 78,
  KFD_API_ID_hsaKmtSetXNACKMode = 79,
  KFD_API_ID_hsaKmtGetXNACKMode = 80,

  KFD_API_ID_NUMBER = 81,
  KFD_API_ID_ANY = 82,
};

// section: API arg structure

typedef struct kfd_api_data_s {
  uint64_t correlation_id;
  uint32_t phase;
  union {
    HSAKMT_STATUS HSAKMT_STATUS_retval;
  };
  union {
    // block: HSAKMTAPI API
    struct {
    } hsaKmtOpenKFD;
    struct {
    } hsaKmtCloseKFD;
    struct {
      HsaVersionInfo* VersionInfo;
    } hsaKmtGetVersion;
    struct {
      HsaSystemProperties* SystemProperties;
    } hsaKmtAcquireSystemProperties;
    struct {
    } hsaKmtReleaseSystemProperties;
    struct {
      HSAuint32               NodeId;
      HsaNodeProperties* NodeProperties;
    } hsaKmtGetNodeProperties;
    struct {
      HSAuint32             NodeId;
      HSAuint32             NumBanks;
      HsaMemoryProperties* MemoryProperties;
    } hsaKmtGetNodeMemoryProperties;
    struct {
      HSAuint32           NodeId;
      HSAuint32           ProcessorId;
      HSAuint32           NumCaches;
      HsaCacheProperties* CacheProperties;
    } hsaKmtGetNodeCacheProperties;
    struct {
      HSAuint32            NodeId;
      HSAuint32            NumIoLinks;
      HsaIoLinkProperties* IoLinkProperties;
    } hsaKmtGetNodeIoLinkProperties;
    struct {
      HsaEventDescriptor* EventDesc;
      bool                ManualReset;
      bool                IsSignaled;
      HsaEvent** Event;
    } hsaKmtCreateEvent;
    struct {
      HsaEvent* Event;
    } hsaKmtDestroyEvent;
    struct {
      HsaEvent* Event;
    } hsaKmtSetEvent;
    struct {
      HsaEvent* Event;
    } hsaKmtResetEvent;
    struct {
      HsaEvent* Event;
    } hsaKmtQueryEventState;
    struct {
      HsaEvent* Event;
      HSAuint32   Milliseconds;
    } hsaKmtWaitOnEvent;
    struct {
      HsaEvent** Events;
      HSAuint32   NumEvents;
      bool        WaitOnAll;
      HSAuint32   Milliseconds;
    } hsaKmtWaitOnMultipleEvents;
    struct {
      HSA_QUEUEID     QueueId;
      HsaQueueReport* QueueReport;
    } hsaKmtReportQueue;
    struct {
      HSAuint32           NodeId;
      HSA_QUEUE_TYPE      Type;
      HSAuint32           QueuePercentage;
      HSA_QUEUE_PRIORITY  Priority;
      void* QueueAddress;
      HSAuint64           QueueSizeInBytes;
      HsaEvent* Event;
      HsaQueueResource* QueueResource;
    } hsaKmtCreateQueue;
    struct {
      HSA_QUEUEID         QueueId;
      HSAuint32           QueuePercentage;
      HSA_QUEUE_PRIORITY  Priority;
      void* QueueAddress;
      HSAuint64           QueueSize;
      HsaEvent* Event;
    } hsaKmtUpdateQueue;
    struct {
      HSA_QUEUEID         QueueId;
    } hsaKmtDestroyQueue;
    struct {
      HSA_QUEUEID         QueueId;
      HSAuint32           CUMaskCount;
      HSAuint32* QueueCUMask;
    } hsaKmtSetQueueCUMask;
    struct {
      HSA_QUEUEID QueueId;
      HsaQueueInfo* QueueInfo;
    } hsaKmtGetQueueInfo;
    struct {
      HSAuint32       Node;
      HSAuint32       DefaultPolicy;
      HSAuint32       AlternatePolicy;
      void* MemoryAddressAlternate;
      HSAuint64       MemorySizeInBytes;
    } hsaKmtSetMemoryPolicy;
    struct {
      HSAuint32       PreferredNode;
      HSAuint64       SizeInBytes;
      HsaMemFlags     MemFlags;
      void** MemoryAddress;
    } hsaKmtAllocMemory;
    struct {
      void* MemoryAddress;
      HSAuint64   SizeInBytes;
    } hsaKmtFreeMemory;
    struct {
      void* MemoryAddress;
      HSAuint64   MemorySizeInBytes;
    } hsaKmtRegisterMemory;
    struct {
      void* MemoryAddress;
      HSAuint64   MemorySizeInBytes;
      HSAuint64   NumberOfNodes;
      HSAuint32* NodeArray;
    } hsaKmtRegisterMemoryToNodes;
    struct {
      void* MemoryAddress;
      HSAuint64   MemorySizeInBytes;
      HsaMemFlags MemFlags;
    } hsaKmtRegisterMemoryWithFlags;
    struct {
      HSAuint64       GraphicsResourceHandle;
      HsaGraphicsResourceInfo* GraphicsResourceInfo;
      HSAuint64       NumberOfNodes;
      HSAuint32* NodeArray;
    } hsaKmtRegisterGraphicsHandleToNodes;
    struct {
      void* MemoryAddress;
      HSAuint64             SizeInBytes;
      HsaSharedMemoryHandle* SharedMemoryHandle;
    } hsaKmtShareMemory;
    struct {
      const HsaSharedMemoryHandle* SharedMemoryHandle;
      void** MemoryAddress;
      HSAuint64* SizeInBytes;
    } hsaKmtRegisterSharedHandle;
    struct {
      const HsaSharedMemoryHandle* SharedMemoryHandle;
      void** MemoryAddress;
      HSAuint64* SizeInBytes;
      HSAuint64                   NumberOfNodes;
      HSAuint32* NodeArray;
    } hsaKmtRegisterSharedHandleToNodes;
    struct {
      HSAuint32                 Pid;
      HsaMemoryRange* LocalMemoryArray;
      HSAuint64                 LocalMemoryArrayCount;
      HsaMemoryRange* RemoteMemoryArray;
      HSAuint64                 RemoteMemoryArrayCount;
      HSAuint64* SizeCopied;
    } hsaKmtProcessVMRead;
    struct {
      HSAuint32                 Pid;
      HsaMemoryRange* LocalMemoryArray;
      HSAuint64                 LocalMemoryArrayCount;
      HsaMemoryRange* RemoteMemoryArray;
      HSAuint64                 RemoteMemoryArrayCount;
      HSAuint64* SizeCopied;
    } hsaKmtProcessVMWrite;
    struct {
      void* MemoryAddress;
    } hsaKmtDeregisterMemory;
    struct {
      void* MemoryAddress;
      HSAuint64       MemorySizeInBytes;
      HSAuint64* AlternateVAGPU;
    } hsaKmtMapMemoryToGPU;
    struct {
      void* MemoryAddress;
      HSAuint64       MemorySizeInBytes;
      HSAuint64* AlternateVAGPU;
      HsaMemMapFlags  MemMapFlags;
      HSAuint64       NumberOfNodes;
      HSAuint32* NodeArray;
    } hsaKmtMapMemoryToGPUNodes;
    struct {
      void* MemoryAddress;
    } hsaKmtUnmapMemoryToGPU;
    struct {
      HSAuint32          NodeId;
      HSAuint64          GraphicDeviceHandle;
      HSAuint64          GraphicResourceHandle;
      HSAuint64          GraphicResourceOffset;
      HSAuint64          GraphicResourceSize;
      HSAuint64* FlatMemoryAddress;
    } hsaKmtMapGraphicHandle;
    struct {
      HSAuint32          NodeId;
      HSAuint64          FlatMemoryAddress;
      HSAuint64              SizeInBytes;
    } hsaKmtUnmapGraphicHandle;
    struct {
      HSA_QUEUEID        QueueId;
      HSAuint32          nGWS;
      HSAuint32* firstGWS;
    } hsaKmtAllocQueueGWS;
    struct {
      HSAuint32       NodeId;
    } hsaKmtDbgRegister;
    struct {
      HSAuint32       NodeId;
    } hsaKmtDbgUnregister;
    struct {
      HSAuint32           NodeId;
      HSA_DBG_WAVEOP      Operand;
      HSA_DBG_WAVEMODE    Mode;
      HSAuint32           TrapId;
      HsaDbgWaveMessage* DbgWaveMsgRing;
    } hsaKmtDbgWavefrontControl;
    struct {
      HSAuint32           NodeId;
      HSAuint32           NumWatchPoints;
      HSA_DBG_WATCH_MODE * WatchMode;
      void** WatchAddress;
      HSAuint64          * WatchMask;
      HsaEvent** WatchEvent;
    } hsaKmtDbgAddressWatch;
    struct {
      HSAuint32    Pid;
      HSAuint32    NumQueues;
      HSA_QUEUEID* Queues;
      HSAuint32    GracePeriod;
      HSAuint32    Flags;
    } hsaKmtQueueSuspend;
    struct {
      HSAuint32   Pid;
      HSAuint32   NumQueues;
      HSA_QUEUEID* Queues;
      HSAuint32   Flags;
    } hsaKmtQueueResume;
    struct {
      HSAuint32	NodeId;
      HSA_QUEUEID	QueueId;
    } hsaKmtEnableDebugTrap;
    struct {
      HSAuint32	NodeId;
      HSA_QUEUEID	QueueId;
      HSAint32* PollFd;
    } hsaKmtEnableDebugTrapWithPollFd;
    struct {
      HSAuint32 NodeId;
    } hsaKmtDisableDebugTrap;
    struct {
      HSAuint32			NodeId;
      HSAuint32			Pid;
      HSAuint32* QueueId;
      bool			ClearEvents;
      HSA_DEBUG_EVENT_TYPE* EventsReceived;
      bool* IsSuspended;
      bool* IsNew;
    } hsaKmtQueryDebugEvent;
    struct {
      HSAuint32			NodeId;
      HSAuint32			Pid;
      bool			ClearEvents;
      void* SnapshotBuf;
      HSAuint32* QssEntries;
    } hsaKmtGetQueueSnapshot;
    struct {
      HSAuint32	NodeId;
      HSAuint32	Pid;
    } hsaKmtSendHostTrap;
    struct {
      HSAuint32             NodeId;
      HSA_DBG_TRAP_OVERRIDE TrapOverride;
      HSA_DBG_TRAP_MASK     TrapMask;
    } hsaKmtSetWaveLaunchTrapOverride;
    struct {
      HSAuint32                NodeId;
      HSA_DBG_WAVE_LAUNCH_MODE WaveLaunchMode;
    } hsaKmtSetWaveLaunchMode;
    struct {
      HSAuint32* Major;
      HSAuint32* Minor;
    } hsaKmtGetKernelDebugTrapVersionInfo;
    struct {
      HSAuint32* Major;
      HSAuint32* Minor;
    } hsaKmtGetThunkDebugTrapVersionInfo;
    struct {
      HSAuint32          NodeId;
      HSAuint32          Pid;
      HSA_DBG_WATCH_MODE WatchMode;
      void* WatchAddress;
      HSAuint64          WatchAddrMask;
      HSAuint32* WatchId;
    } hsaKmtSetAddressWatch;
    struct {
      HSAuint32 NodeId;
      HSAuint32 Pid;
      HSAuint32 WatchId;
    } hsaKmtClearAddressWatch;
    struct {
      HSAuint32 NodeId;
    } hsaKmtEnablePreciseMemoryOperations;
    struct {
      HSAuint32 NodeId;
    } hsaKmtDisablePreciseMemoryOperations;
    struct {
      HSAuint32         NodeId;
      HsaClockCounters* Counters;
    } hsaKmtGetClockCounters;
    struct {
      HSAuint32                   NodeId;
      HsaCounterProperties** CounterProperties;
    } hsaKmtPmcGetCounterProperties;
    struct {
      HSAuint32           NodeId;
      HSAuint32           NumberOfCounters;
      HsaCounter* Counters;
      HsaPmcTraceRoot* TraceRoot;
    } hsaKmtPmcRegisterTrace;
    struct {
      HSAuint32   NodeId;
      HSATraceId  TraceId;
    } hsaKmtPmcUnregisterTrace;
    struct {
      HSAuint32   NodeId;
      HSATraceId  TraceId;
    } hsaKmtPmcAcquireTraceAccess;
    struct {
      HSAuint32   NodeId;
      HSATraceId  TraceId;
    } hsaKmtPmcReleaseTraceAccess;
    struct {
      HSATraceId  TraceId;
      void* TraceBuffer;
      HSAuint64   TraceBufferSizeBytes;
    } hsaKmtPmcStartTrace;
    struct {
      HSATraceId    TraceId;
    } hsaKmtPmcQueryTrace;
    struct {
      HSATraceId  TraceId;
    } hsaKmtPmcStopTrace;
    struct {
      HSAuint32           NodeId;
      void* TrapHandlerBaseAddress;
      HSAuint64           TrapHandlerSizeInBytes;
      void* TrapBufferBaseAddress;
      HSAuint64           TrapBufferSizeInBytes;
    } hsaKmtSetTrapHandler;
    struct {
      HSAuint32           NodeId;
      HsaGpuTileConfig* config;
    } hsaKmtGetTileConfig;
    struct {
      const void* Pointer;
      HsaPointerInfo* PointerInfo;
    } hsaKmtQueryPointerInfo;
    struct {
      const void* Pointer;
      void* UserData;
    } hsaKmtSetMemoryUserData;
    struct {
      HSAuint32	PreferredNode;
    } hsaKmtSPMAcquire;
    struct {
      HSAuint32	PreferredNode;
    } hsaKmtSPMRelease;
    struct {
      HSAuint32   PreferredNode;
      HSAuint32   SizeInBytes;
      HSAuint32* timeout;
      HSAuint32* SizeCopied;
      void* DestMemoryAddress;
      bool* isSPMDataLoss;
    } hsaKmtSPMSetDestBuffer;
    struct {
      void* start_addr;
      HSAuint64 size;
      unsigned int nattr;
      HSA_SVM_ATTRIBUTE* attrs;
    } hsaKmtSVMSetAttr;
    struct {
      void* start_addr;
      HSAuint64 size;
      unsigned int nattr;
      HSA_SVM_ATTRIBUTE* attrs;
    } hsaKmtSVMGetAttr;
    struct {
      HSAint32 enable;
    } hsaKmtSetXNACKMode;
    struct {
      HSAint32* enable;
    } hsaKmtGetXNACKMode;
  } args;
} kfd_api_data_t;

#if PROF_API_IMPL
#include <roctracer_cb_table.h>
namespace roctracer {
namespace kfd_support {

// section: API get_name function

const char* GetApiName(const uint32_t& id) {
  switch (id) {
    // block: HSAKMTAPI API
    case KFD_API_ID_hsaKmtOpenKFD: return "hsaKmtOpenKFD";
    case KFD_API_ID_hsaKmtCloseKFD: return "hsaKmtCloseKFD";
    case KFD_API_ID_hsaKmtGetVersion: return "hsaKmtGetVersion";
    case KFD_API_ID_hsaKmtAcquireSystemProperties: return "hsaKmtAcquireSystemProperties";
    case KFD_API_ID_hsaKmtReleaseSystemProperties: return "hsaKmtReleaseSystemProperties";
    case KFD_API_ID_hsaKmtGetNodeProperties: return "hsaKmtGetNodeProperties";
    case KFD_API_ID_hsaKmtGetNodeMemoryProperties: return "hsaKmtGetNodeMemoryProperties";
    case KFD_API_ID_hsaKmtGetNodeCacheProperties: return "hsaKmtGetNodeCacheProperties";
    case KFD_API_ID_hsaKmtGetNodeIoLinkProperties: return "hsaKmtGetNodeIoLinkProperties";
    case KFD_API_ID_hsaKmtCreateEvent: return "hsaKmtCreateEvent";
    case KFD_API_ID_hsaKmtDestroyEvent: return "hsaKmtDestroyEvent";
    case KFD_API_ID_hsaKmtSetEvent: return "hsaKmtSetEvent";
    case KFD_API_ID_hsaKmtResetEvent: return "hsaKmtResetEvent";
    case KFD_API_ID_hsaKmtQueryEventState: return "hsaKmtQueryEventState";
    case KFD_API_ID_hsaKmtWaitOnEvent: return "hsaKmtWaitOnEvent";
    case KFD_API_ID_hsaKmtWaitOnMultipleEvents: return "hsaKmtWaitOnMultipleEvents";
    case KFD_API_ID_hsaKmtReportQueue: return "hsaKmtReportQueue";
    case KFD_API_ID_hsaKmtCreateQueue: return "hsaKmtCreateQueue";
    case KFD_API_ID_hsaKmtUpdateQueue: return "hsaKmtUpdateQueue";
    case KFD_API_ID_hsaKmtDestroyQueue: return "hsaKmtDestroyQueue";
    case KFD_API_ID_hsaKmtSetQueueCUMask: return "hsaKmtSetQueueCUMask";
    case KFD_API_ID_hsaKmtGetQueueInfo: return "hsaKmtGetQueueInfo";
    case KFD_API_ID_hsaKmtSetMemoryPolicy: return "hsaKmtSetMemoryPolicy";
    case KFD_API_ID_hsaKmtAllocMemory: return "hsaKmtAllocMemory";
    case KFD_API_ID_hsaKmtFreeMemory: return "hsaKmtFreeMemory";
    case KFD_API_ID_hsaKmtRegisterMemory: return "hsaKmtRegisterMemory";
    case KFD_API_ID_hsaKmtRegisterMemoryToNodes: return "hsaKmtRegisterMemoryToNodes";
    case KFD_API_ID_hsaKmtRegisterMemoryWithFlags: return "hsaKmtRegisterMemoryWithFlags";
    case KFD_API_ID_hsaKmtRegisterGraphicsHandleToNodes: return "hsaKmtRegisterGraphicsHandleToNodes";
    case KFD_API_ID_hsaKmtShareMemory: return "hsaKmtShareMemory";
    case KFD_API_ID_hsaKmtRegisterSharedHandle: return "hsaKmtRegisterSharedHandle";
    case KFD_API_ID_hsaKmtRegisterSharedHandleToNodes: return "hsaKmtRegisterSharedHandleToNodes";
    case KFD_API_ID_hsaKmtProcessVMRead: return "hsaKmtProcessVMRead";
    case KFD_API_ID_hsaKmtProcessVMWrite: return "hsaKmtProcessVMWrite";
    case KFD_API_ID_hsaKmtDeregisterMemory: return "hsaKmtDeregisterMemory";
    case KFD_API_ID_hsaKmtMapMemoryToGPU: return "hsaKmtMapMemoryToGPU";
    case KFD_API_ID_hsaKmtMapMemoryToGPUNodes: return "hsaKmtMapMemoryToGPUNodes";
    case KFD_API_ID_hsaKmtUnmapMemoryToGPU: return "hsaKmtUnmapMemoryToGPU";
    case KFD_API_ID_hsaKmtMapGraphicHandle: return "hsaKmtMapGraphicHandle";
    case KFD_API_ID_hsaKmtUnmapGraphicHandle: return "hsaKmtUnmapGraphicHandle";
    case KFD_API_ID_hsaKmtAllocQueueGWS: return "hsaKmtAllocQueueGWS";
    case KFD_API_ID_hsaKmtDbgRegister: return "hsaKmtDbgRegister";
    case KFD_API_ID_hsaKmtDbgUnregister: return "hsaKmtDbgUnregister";
    case KFD_API_ID_hsaKmtDbgWavefrontControl: return "hsaKmtDbgWavefrontControl";
    case KFD_API_ID_hsaKmtDbgAddressWatch: return "hsaKmtDbgAddressWatch";
    case KFD_API_ID_hsaKmtQueueSuspend: return "hsaKmtQueueSuspend";
    case KFD_API_ID_hsaKmtQueueResume: return "hsaKmtQueueResume";
    case KFD_API_ID_hsaKmtEnableDebugTrap: return "hsaKmtEnableDebugTrap";
    case KFD_API_ID_hsaKmtEnableDebugTrapWithPollFd: return "hsaKmtEnableDebugTrapWithPollFd";
    case KFD_API_ID_hsaKmtDisableDebugTrap: return "hsaKmtDisableDebugTrap";
    case KFD_API_ID_hsaKmtQueryDebugEvent: return "hsaKmtQueryDebugEvent";
    case KFD_API_ID_hsaKmtGetQueueSnapshot: return "hsaKmtGetQueueSnapshot";
    case KFD_API_ID_hsaKmtSendHostTrap: return "hsaKmtSendHostTrap";
    case KFD_API_ID_hsaKmtSetWaveLaunchTrapOverride: return "hsaKmtSetWaveLaunchTrapOverride";
    case KFD_API_ID_hsaKmtSetWaveLaunchMode: return "hsaKmtSetWaveLaunchMode";
    case KFD_API_ID_hsaKmtGetKernelDebugTrapVersionInfo: return "hsaKmtGetKernelDebugTrapVersionInfo";
    case KFD_API_ID_hsaKmtGetThunkDebugTrapVersionInfo: return "hsaKmtGetThunkDebugTrapVersionInfo";
    case KFD_API_ID_hsaKmtSetAddressWatch: return "hsaKmtSetAddressWatch";
    case KFD_API_ID_hsaKmtClearAddressWatch: return "hsaKmtClearAddressWatch";
    case KFD_API_ID_hsaKmtEnablePreciseMemoryOperations: return "hsaKmtEnablePreciseMemoryOperations";
    case KFD_API_ID_hsaKmtDisablePreciseMemoryOperations: return "hsaKmtDisablePreciseMemoryOperations";
    case KFD_API_ID_hsaKmtGetClockCounters: return "hsaKmtGetClockCounters";
    case KFD_API_ID_hsaKmtPmcGetCounterProperties: return "hsaKmtPmcGetCounterProperties";
    case KFD_API_ID_hsaKmtPmcRegisterTrace: return "hsaKmtPmcRegisterTrace";
    case KFD_API_ID_hsaKmtPmcUnregisterTrace: return "hsaKmtPmcUnregisterTrace";
    case KFD_API_ID_hsaKmtPmcAcquireTraceAccess: return "hsaKmtPmcAcquireTraceAccess";
    case KFD_API_ID_hsaKmtPmcReleaseTraceAccess: return "hsaKmtPmcReleaseTraceAccess";
    case KFD_API_ID_hsaKmtPmcStartTrace: return "hsaKmtPmcStartTrace";
    case KFD_API_ID_hsaKmtPmcQueryTrace: return "hsaKmtPmcQueryTrace";
    case KFD_API_ID_hsaKmtPmcStopTrace: return "hsaKmtPmcStopTrace";
    case KFD_API_ID_hsaKmtSetTrapHandler: return "hsaKmtSetTrapHandler";
    case KFD_API_ID_hsaKmtGetTileConfig: return "hsaKmtGetTileConfig";
    case KFD_API_ID_hsaKmtQueryPointerInfo: return "hsaKmtQueryPointerInfo";
    case KFD_API_ID_hsaKmtSetMemoryUserData: return "hsaKmtSetMemoryUserData";
    case KFD_API_ID_hsaKmtSPMAcquire: return "hsaKmtSPMAcquire";
    case KFD_API_ID_hsaKmtSPMRelease: return "hsaKmtSPMRelease";
    case KFD_API_ID_hsaKmtSPMSetDestBuffer: return "hsaKmtSPMSetDestBuffer";
    case KFD_API_ID_hsaKmtSVMSetAttr: return "hsaKmtSVMSetAttr";
    case KFD_API_ID_hsaKmtSVMGetAttr: return "hsaKmtSVMGetAttr";
    case KFD_API_ID_hsaKmtSetXNACKMode: return "hsaKmtSetXNACKMode";
    case KFD_API_ID_hsaKmtGetXNACKMode: return "hsaKmtGetXNACKMode";
  }
  return "unknown";
}

// section: API get_code function

uint32_t GetApiCode(const char* str) {
  // block: HSAKMTAPI API
  if (strcmp("hsaKmtOpenKFD", str) == 0) return KFD_API_ID_hsaKmtOpenKFD;
  if (strcmp("hsaKmtCloseKFD", str) == 0) return KFD_API_ID_hsaKmtCloseKFD;
  if (strcmp("hsaKmtGetVersion", str) == 0) return KFD_API_ID_hsaKmtGetVersion;
  if (strcmp("hsaKmtAcquireSystemProperties", str) == 0) return KFD_API_ID_hsaKmtAcquireSystemProperties;
  if (strcmp("hsaKmtReleaseSystemProperties", str) == 0) return KFD_API_ID_hsaKmtReleaseSystemProperties;
  if (strcmp("hsaKmtGetNodeProperties", str) == 0) return KFD_API_ID_hsaKmtGetNodeProperties;
  if (strcmp("hsaKmtGetNodeMemoryProperties", str) == 0) return KFD_API_ID_hsaKmtGetNodeMemoryProperties;
  if (strcmp("hsaKmtGetNodeCacheProperties", str) == 0) return KFD_API_ID_hsaKmtGetNodeCacheProperties;
  if (strcmp("hsaKmtGetNodeIoLinkProperties", str) == 0) return KFD_API_ID_hsaKmtGetNodeIoLinkProperties;
  if (strcmp("hsaKmtCreateEvent", str) == 0) return KFD_API_ID_hsaKmtCreateEvent;
  if (strcmp("hsaKmtDestroyEvent", str) == 0) return KFD_API_ID_hsaKmtDestroyEvent;
  if (strcmp("hsaKmtSetEvent", str) == 0) return KFD_API_ID_hsaKmtSetEvent;
  if (strcmp("hsaKmtResetEvent", str) == 0) return KFD_API_ID_hsaKmtResetEvent;
  if (strcmp("hsaKmtQueryEventState", str) == 0) return KFD_API_ID_hsaKmtQueryEventState;
  if (strcmp("hsaKmtWaitOnEvent", str) == 0) return KFD_API_ID_hsaKmtWaitOnEvent;
  if (strcmp("hsaKmtWaitOnMultipleEvents", str) == 0) return KFD_API_ID_hsaKmtWaitOnMultipleEvents;
  if (strcmp("hsaKmtReportQueue", str) == 0) return KFD_API_ID_hsaKmtReportQueue;
  if (strcmp("hsaKmtCreateQueue", str) == 0) return KFD_API_ID_hsaKmtCreateQueue;
  if (strcmp("hsaKmtUpdateQueue", str) == 0) return KFD_API_ID_hsaKmtUpdateQueue;
  if (strcmp("hsaKmtDestroyQueue", str) == 0) return KFD_API_ID_hsaKmtDestroyQueue;
  if (strcmp("hsaKmtSetQueueCUMask", str) == 0) return KFD_API_ID_hsaKmtSetQueueCUMask;
  if (strcmp("hsaKmtGetQueueInfo", str) == 0) return KFD_API_ID_hsaKmtGetQueueInfo;
  if (strcmp("hsaKmtSetMemoryPolicy", str) == 0) return KFD_API_ID_hsaKmtSetMemoryPolicy;
  if (strcmp("hsaKmtAllocMemory", str) == 0) return KFD_API_ID_hsaKmtAllocMemory;
  if (strcmp("hsaKmtFreeMemory", str) == 0) return KFD_API_ID_hsaKmtFreeMemory;
  if (strcmp("hsaKmtRegisterMemory", str) == 0) return KFD_API_ID_hsaKmtRegisterMemory;
  if (strcmp("hsaKmtRegisterMemoryToNodes", str) == 0) return KFD_API_ID_hsaKmtRegisterMemoryToNodes;
  if (strcmp("hsaKmtRegisterMemoryWithFlags", str) == 0) return KFD_API_ID_hsaKmtRegisterMemoryWithFlags;
  if (strcmp("hsaKmtRegisterGraphicsHandleToNodes", str) == 0) return KFD_API_ID_hsaKmtRegisterGraphicsHandleToNodes;
  if (strcmp("hsaKmtShareMemory", str) == 0) return KFD_API_ID_hsaKmtShareMemory;
  if (strcmp("hsaKmtRegisterSharedHandle", str) == 0) return KFD_API_ID_hsaKmtRegisterSharedHandle;
  if (strcmp("hsaKmtRegisterSharedHandleToNodes", str) == 0) return KFD_API_ID_hsaKmtRegisterSharedHandleToNodes;
  if (strcmp("hsaKmtProcessVMRead", str) == 0) return KFD_API_ID_hsaKmtProcessVMRead;
  if (strcmp("hsaKmtProcessVMWrite", str) == 0) return KFD_API_ID_hsaKmtProcessVMWrite;
  if (strcmp("hsaKmtDeregisterMemory", str) == 0) return KFD_API_ID_hsaKmtDeregisterMemory;
  if (strcmp("hsaKmtMapMemoryToGPU", str) == 0) return KFD_API_ID_hsaKmtMapMemoryToGPU;
  if (strcmp("hsaKmtMapMemoryToGPUNodes", str) == 0) return KFD_API_ID_hsaKmtMapMemoryToGPUNodes;
  if (strcmp("hsaKmtUnmapMemoryToGPU", str) == 0) return KFD_API_ID_hsaKmtUnmapMemoryToGPU;
  if (strcmp("hsaKmtMapGraphicHandle", str) == 0) return KFD_API_ID_hsaKmtMapGraphicHandle;
  if (strcmp("hsaKmtUnmapGraphicHandle", str) == 0) return KFD_API_ID_hsaKmtUnmapGraphicHandle;
  if (strcmp("hsaKmtAllocQueueGWS", str) == 0) return KFD_API_ID_hsaKmtAllocQueueGWS;
  if (strcmp("hsaKmtDbgRegister", str) == 0) return KFD_API_ID_hsaKmtDbgRegister;
  if (strcmp("hsaKmtDbgUnregister", str) == 0) return KFD_API_ID_hsaKmtDbgUnregister;
  if (strcmp("hsaKmtDbgWavefrontControl", str) == 0) return KFD_API_ID_hsaKmtDbgWavefrontControl;
  if (strcmp("hsaKmtDbgAddressWatch", str) == 0) return KFD_API_ID_hsaKmtDbgAddressWatch;
  if (strcmp("hsaKmtQueueSuspend", str) == 0) return KFD_API_ID_hsaKmtQueueSuspend;
  if (strcmp("hsaKmtQueueResume", str) == 0) return KFD_API_ID_hsaKmtQueueResume;
  if (strcmp("hsaKmtEnableDebugTrap", str) == 0) return KFD_API_ID_hsaKmtEnableDebugTrap;
  if (strcmp("hsaKmtEnableDebugTrapWithPollFd", str) == 0) return KFD_API_ID_hsaKmtEnableDebugTrapWithPollFd;
  if (strcmp("hsaKmtDisableDebugTrap", str) == 0) return KFD_API_ID_hsaKmtDisableDebugTrap;
  if (strcmp("hsaKmtQueryDebugEvent", str) == 0) return KFD_API_ID_hsaKmtQueryDebugEvent;
  if (strcmp("hsaKmtGetQueueSnapshot", str) == 0) return KFD_API_ID_hsaKmtGetQueueSnapshot;
  if (strcmp("hsaKmtSendHostTrap", str) == 0) return KFD_API_ID_hsaKmtSendHostTrap;
  if (strcmp("hsaKmtSetWaveLaunchTrapOverride", str) == 0) return KFD_API_ID_hsaKmtSetWaveLaunchTrapOverride;
  if (strcmp("hsaKmtSetWaveLaunchMode", str) == 0) return KFD_API_ID_hsaKmtSetWaveLaunchMode;
  if (strcmp("hsaKmtGetKernelDebugTrapVersionInfo", str) == 0) return KFD_API_ID_hsaKmtGetKernelDebugTrapVersionInfo;
  if (strcmp("hsaKmtGetThunkDebugTrapVersionInfo", str) == 0) return KFD_API_ID_hsaKmtGetThunkDebugTrapVersionInfo;
  if (strcmp("hsaKmtSetAddressWatch", str) == 0) return KFD_API_ID_hsaKmtSetAddressWatch;
  if (strcmp("hsaKmtClearAddressWatch", str) == 0) return KFD_API_ID_hsaKmtClearAddressWatch;
  if (strcmp("hsaKmtEnablePreciseMemoryOperations", str) == 0) return KFD_API_ID_hsaKmtEnablePreciseMemoryOperations;
  if (strcmp("hsaKmtDisablePreciseMemoryOperations", str) == 0) return KFD_API_ID_hsaKmtDisablePreciseMemoryOperations;
  if (strcmp("hsaKmtGetClockCounters", str) == 0) return KFD_API_ID_hsaKmtGetClockCounters;
  if (strcmp("hsaKmtPmcGetCounterProperties", str) == 0) return KFD_API_ID_hsaKmtPmcGetCounterProperties;
  if (strcmp("hsaKmtPmcRegisterTrace", str) == 0) return KFD_API_ID_hsaKmtPmcRegisterTrace;
  if (strcmp("hsaKmtPmcUnregisterTrace", str) == 0) return KFD_API_ID_hsaKmtPmcUnregisterTrace;
  if (strcmp("hsaKmtPmcAcquireTraceAccess", str) == 0) return KFD_API_ID_hsaKmtPmcAcquireTraceAccess;
  if (strcmp("hsaKmtPmcReleaseTraceAccess", str) == 0) return KFD_API_ID_hsaKmtPmcReleaseTraceAccess;
  if (strcmp("hsaKmtPmcStartTrace", str) == 0) return KFD_API_ID_hsaKmtPmcStartTrace;
  if (strcmp("hsaKmtPmcQueryTrace", str) == 0) return KFD_API_ID_hsaKmtPmcQueryTrace;
  if (strcmp("hsaKmtPmcStopTrace", str) == 0) return KFD_API_ID_hsaKmtPmcStopTrace;
  if (strcmp("hsaKmtSetTrapHandler", str) == 0) return KFD_API_ID_hsaKmtSetTrapHandler;
  if (strcmp("hsaKmtGetTileConfig", str) == 0) return KFD_API_ID_hsaKmtGetTileConfig;
  if (strcmp("hsaKmtQueryPointerInfo", str) == 0) return KFD_API_ID_hsaKmtQueryPointerInfo;
  if (strcmp("hsaKmtSetMemoryUserData", str) == 0) return KFD_API_ID_hsaKmtSetMemoryUserData;
  if (strcmp("hsaKmtSPMAcquire", str) == 0) return KFD_API_ID_hsaKmtSPMAcquire;
  if (strcmp("hsaKmtSPMRelease", str) == 0) return KFD_API_ID_hsaKmtSPMRelease;
  if (strcmp("hsaKmtSPMSetDestBuffer", str) == 0) return KFD_API_ID_hsaKmtSPMSetDestBuffer;
  if (strcmp("hsaKmtSVMSetAttr", str) == 0) return KFD_API_ID_hsaKmtSVMSetAttr;
  if (strcmp("hsaKmtSVMGetAttr", str) == 0) return KFD_API_ID_hsaKmtSVMGetAttr;
  if (strcmp("hsaKmtSetXNACKMode", str) == 0) return KFD_API_ID_hsaKmtSetXNACKMode;
  if (strcmp("hsaKmtGetXNACKMode", str) == 0) return KFD_API_ID_hsaKmtGetXNACKMode;
  return KFD_API_ID_NUMBER;
}

// section: API intercepting code

// block: HSAKMTAPI API
typedef struct {
  decltype(hsaKmtOpenKFD)* hsaKmtOpenKFD_fn;
  decltype(hsaKmtCloseKFD)* hsaKmtCloseKFD_fn;
  decltype(hsaKmtGetVersion)* hsaKmtGetVersion_fn;
  decltype(hsaKmtAcquireSystemProperties)* hsaKmtAcquireSystemProperties_fn;
  decltype(hsaKmtReleaseSystemProperties)* hsaKmtReleaseSystemProperties_fn;
  decltype(hsaKmtGetNodeProperties)* hsaKmtGetNodeProperties_fn;
  decltype(hsaKmtGetNodeMemoryProperties)* hsaKmtGetNodeMemoryProperties_fn;
  decltype(hsaKmtGetNodeCacheProperties)* hsaKmtGetNodeCacheProperties_fn;
  decltype(hsaKmtGetNodeIoLinkProperties)* hsaKmtGetNodeIoLinkProperties_fn;
  decltype(hsaKmtCreateEvent)* hsaKmtCreateEvent_fn;
  decltype(hsaKmtDestroyEvent)* hsaKmtDestroyEvent_fn;
  decltype(hsaKmtSetEvent)* hsaKmtSetEvent_fn;
  decltype(hsaKmtResetEvent)* hsaKmtResetEvent_fn;
  decltype(hsaKmtQueryEventState)* hsaKmtQueryEventState_fn;
  decltype(hsaKmtWaitOnEvent)* hsaKmtWaitOnEvent_fn;
  decltype(hsaKmtWaitOnMultipleEvents)* hsaKmtWaitOnMultipleEvents_fn;
  decltype(hsaKmtReportQueue)* hsaKmtReportQueue_fn;
  decltype(hsaKmtCreateQueue)* hsaKmtCreateQueue_fn;
  decltype(hsaKmtUpdateQueue)* hsaKmtUpdateQueue_fn;
  decltype(hsaKmtDestroyQueue)* hsaKmtDestroyQueue_fn;
  decltype(hsaKmtSetQueueCUMask)* hsaKmtSetQueueCUMask_fn;
  decltype(hsaKmtGetQueueInfo)* hsaKmtGetQueueInfo_fn;
  decltype(hsaKmtSetMemoryPolicy)* hsaKmtSetMemoryPolicy_fn;
  decltype(hsaKmtAllocMemory)* hsaKmtAllocMemory_fn;
  decltype(hsaKmtFreeMemory)* hsaKmtFreeMemory_fn;
  decltype(hsaKmtRegisterMemory)* hsaKmtRegisterMemory_fn;
  decltype(hsaKmtRegisterMemoryToNodes)* hsaKmtRegisterMemoryToNodes_fn;
  decltype(hsaKmtRegisterMemoryWithFlags)* hsaKmtRegisterMemoryWithFlags_fn;
  decltype(hsaKmtRegisterGraphicsHandleToNodes)* hsaKmtRegisterGraphicsHandleToNodes_fn;
  decltype(hsaKmtShareMemory)* hsaKmtShareMemory_fn;
  decltype(hsaKmtRegisterSharedHandle)* hsaKmtRegisterSharedHandle_fn;
  decltype(hsaKmtRegisterSharedHandleToNodes)* hsaKmtRegisterSharedHandleToNodes_fn;
  decltype(hsaKmtProcessVMRead)* hsaKmtProcessVMRead_fn;
  decltype(hsaKmtProcessVMWrite)* hsaKmtProcessVMWrite_fn;
  decltype(hsaKmtDeregisterMemory)* hsaKmtDeregisterMemory_fn;
  decltype(hsaKmtMapMemoryToGPU)* hsaKmtMapMemoryToGPU_fn;
  decltype(hsaKmtMapMemoryToGPUNodes)* hsaKmtMapMemoryToGPUNodes_fn;
  decltype(hsaKmtUnmapMemoryToGPU)* hsaKmtUnmapMemoryToGPU_fn;
  decltype(hsaKmtMapGraphicHandle)* hsaKmtMapGraphicHandle_fn;
  decltype(hsaKmtUnmapGraphicHandle)* hsaKmtUnmapGraphicHandle_fn;
  decltype(hsaKmtAllocQueueGWS)* hsaKmtAllocQueueGWS_fn;
  decltype(hsaKmtDbgRegister)* hsaKmtDbgRegister_fn;
  decltype(hsaKmtDbgUnregister)* hsaKmtDbgUnregister_fn;
  decltype(hsaKmtDbgWavefrontControl)* hsaKmtDbgWavefrontControl_fn;
  decltype(hsaKmtDbgAddressWatch)* hsaKmtDbgAddressWatch_fn;
  decltype(hsaKmtQueueSuspend)* hsaKmtQueueSuspend_fn;
  decltype(hsaKmtQueueResume)* hsaKmtQueueResume_fn;
  decltype(hsaKmtEnableDebugTrap)* hsaKmtEnableDebugTrap_fn;
  decltype(hsaKmtEnableDebugTrapWithPollFd)* hsaKmtEnableDebugTrapWithPollFd_fn;
  decltype(hsaKmtDisableDebugTrap)* hsaKmtDisableDebugTrap_fn;
  decltype(hsaKmtQueryDebugEvent)* hsaKmtQueryDebugEvent_fn;
  decltype(hsaKmtGetQueueSnapshot)* hsaKmtGetQueueSnapshot_fn;
  decltype(hsaKmtSendHostTrap)* hsaKmtSendHostTrap_fn;
  decltype(hsaKmtSetWaveLaunchTrapOverride)* hsaKmtSetWaveLaunchTrapOverride_fn;
  decltype(hsaKmtSetWaveLaunchMode)* hsaKmtSetWaveLaunchMode_fn;
  decltype(hsaKmtGetKernelDebugTrapVersionInfo)* hsaKmtGetKernelDebugTrapVersionInfo_fn;
  decltype(hsaKmtGetThunkDebugTrapVersionInfo)* hsaKmtGetThunkDebugTrapVersionInfo_fn;
  decltype(hsaKmtSetAddressWatch)* hsaKmtSetAddressWatch_fn;
  decltype(hsaKmtClearAddressWatch)* hsaKmtClearAddressWatch_fn;
  decltype(hsaKmtEnablePreciseMemoryOperations)* hsaKmtEnablePreciseMemoryOperations_fn;
  decltype(hsaKmtDisablePreciseMemoryOperations)* hsaKmtDisablePreciseMemoryOperations_fn;
  decltype(hsaKmtGetClockCounters)* hsaKmtGetClockCounters_fn;
  decltype(hsaKmtPmcGetCounterProperties)* hsaKmtPmcGetCounterProperties_fn;
  decltype(hsaKmtPmcRegisterTrace)* hsaKmtPmcRegisterTrace_fn;
  decltype(hsaKmtPmcUnregisterTrace)* hsaKmtPmcUnregisterTrace_fn;
  decltype(hsaKmtPmcAcquireTraceAccess)* hsaKmtPmcAcquireTraceAccess_fn;
  decltype(hsaKmtPmcReleaseTraceAccess)* hsaKmtPmcReleaseTraceAccess_fn;
  decltype(hsaKmtPmcStartTrace)* hsaKmtPmcStartTrace_fn;
  decltype(hsaKmtPmcQueryTrace)* hsaKmtPmcQueryTrace_fn;
  decltype(hsaKmtPmcStopTrace)* hsaKmtPmcStopTrace_fn;
  decltype(hsaKmtSetTrapHandler)* hsaKmtSetTrapHandler_fn;
  decltype(hsaKmtGetTileConfig)* hsaKmtGetTileConfig_fn;
  decltype(hsaKmtQueryPointerInfo)* hsaKmtQueryPointerInfo_fn;
  decltype(hsaKmtSetMemoryUserData)* hsaKmtSetMemoryUserData_fn;
  decltype(hsaKmtSPMAcquire)* hsaKmtSPMAcquire_fn;
  decltype(hsaKmtSPMRelease)* hsaKmtSPMRelease_fn;
  decltype(hsaKmtSPMSetDestBuffer)* hsaKmtSPMSetDestBuffer_fn;
  decltype(hsaKmtSVMSetAttr)* hsaKmtSVMSetAttr_fn;
  decltype(hsaKmtSVMGetAttr)* hsaKmtSVMGetAttr_fn;
  decltype(hsaKmtSetXNACKMode)* hsaKmtSetXNACKMode_fn;
  decltype(hsaKmtGetXNACKMode)* hsaKmtGetXNACKMode_fn;
} HSAKMTAPI_table_t;

// section: API intercepting code

// block: HSAKMTAPI API
HSAKMTAPI_table_t* HSAKMTAPI_table = NULL;
void intercept_KFDApiTable(void) {
  HSAKMTAPI_table = new HSAKMTAPI_table_t{};
  typedef decltype(HSAKMTAPI_table_t::hsaKmtOpenKFD_fn) hsaKmtOpenKFD_t;
  HSAKMTAPI_table->hsaKmtOpenKFD_fn = (hsaKmtOpenKFD_t)dlsym(RTLD_NEXT,"hsaKmtOpenKFD");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtCloseKFD_fn) hsaKmtCloseKFD_t;
  HSAKMTAPI_table->hsaKmtCloseKFD_fn = (hsaKmtCloseKFD_t)dlsym(RTLD_NEXT,"hsaKmtCloseKFD");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetVersion_fn) hsaKmtGetVersion_t;
  HSAKMTAPI_table->hsaKmtGetVersion_fn = (hsaKmtGetVersion_t)dlsym(RTLD_NEXT,"hsaKmtGetVersion");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtAcquireSystemProperties_fn) hsaKmtAcquireSystemProperties_t;
  HSAKMTAPI_table->hsaKmtAcquireSystemProperties_fn = (hsaKmtAcquireSystemProperties_t)dlsym(RTLD_NEXT,"hsaKmtAcquireSystemProperties");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtReleaseSystemProperties_fn) hsaKmtReleaseSystemProperties_t;
  HSAKMTAPI_table->hsaKmtReleaseSystemProperties_fn = (hsaKmtReleaseSystemProperties_t)dlsym(RTLD_NEXT,"hsaKmtReleaseSystemProperties");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetNodeProperties_fn) hsaKmtGetNodeProperties_t;
  HSAKMTAPI_table->hsaKmtGetNodeProperties_fn = (hsaKmtGetNodeProperties_t)dlsym(RTLD_NEXT,"hsaKmtGetNodeProperties");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetNodeMemoryProperties_fn) hsaKmtGetNodeMemoryProperties_t;
  HSAKMTAPI_table->hsaKmtGetNodeMemoryProperties_fn = (hsaKmtGetNodeMemoryProperties_t)dlsym(RTLD_NEXT,"hsaKmtGetNodeMemoryProperties");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetNodeCacheProperties_fn) hsaKmtGetNodeCacheProperties_t;
  HSAKMTAPI_table->hsaKmtGetNodeCacheProperties_fn = (hsaKmtGetNodeCacheProperties_t)dlsym(RTLD_NEXT,"hsaKmtGetNodeCacheProperties");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetNodeIoLinkProperties_fn) hsaKmtGetNodeIoLinkProperties_t;
  HSAKMTAPI_table->hsaKmtGetNodeIoLinkProperties_fn = (hsaKmtGetNodeIoLinkProperties_t)dlsym(RTLD_NEXT,"hsaKmtGetNodeIoLinkProperties");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtCreateEvent_fn) hsaKmtCreateEvent_t;
  HSAKMTAPI_table->hsaKmtCreateEvent_fn = (hsaKmtCreateEvent_t)dlsym(RTLD_NEXT,"hsaKmtCreateEvent");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtDestroyEvent_fn) hsaKmtDestroyEvent_t;
  HSAKMTAPI_table->hsaKmtDestroyEvent_fn = (hsaKmtDestroyEvent_t)dlsym(RTLD_NEXT,"hsaKmtDestroyEvent");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSetEvent_fn) hsaKmtSetEvent_t;
  HSAKMTAPI_table->hsaKmtSetEvent_fn = (hsaKmtSetEvent_t)dlsym(RTLD_NEXT,"hsaKmtSetEvent");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtResetEvent_fn) hsaKmtResetEvent_t;
  HSAKMTAPI_table->hsaKmtResetEvent_fn = (hsaKmtResetEvent_t)dlsym(RTLD_NEXT,"hsaKmtResetEvent");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtQueryEventState_fn) hsaKmtQueryEventState_t;
  HSAKMTAPI_table->hsaKmtQueryEventState_fn = (hsaKmtQueryEventState_t)dlsym(RTLD_NEXT,"hsaKmtQueryEventState");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtWaitOnEvent_fn) hsaKmtWaitOnEvent_t;
  HSAKMTAPI_table->hsaKmtWaitOnEvent_fn = (hsaKmtWaitOnEvent_t)dlsym(RTLD_NEXT,"hsaKmtWaitOnEvent");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtWaitOnMultipleEvents_fn) hsaKmtWaitOnMultipleEvents_t;
  HSAKMTAPI_table->hsaKmtWaitOnMultipleEvents_fn = (hsaKmtWaitOnMultipleEvents_t)dlsym(RTLD_NEXT,"hsaKmtWaitOnMultipleEvents");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtReportQueue_fn) hsaKmtReportQueue_t;
  HSAKMTAPI_table->hsaKmtReportQueue_fn = (hsaKmtReportQueue_t)dlsym(RTLD_NEXT,"hsaKmtReportQueue");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtCreateQueue_fn) hsaKmtCreateQueue_t;
  HSAKMTAPI_table->hsaKmtCreateQueue_fn = (hsaKmtCreateQueue_t)dlsym(RTLD_NEXT,"hsaKmtCreateQueue");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtUpdateQueue_fn) hsaKmtUpdateQueue_t;
  HSAKMTAPI_table->hsaKmtUpdateQueue_fn = (hsaKmtUpdateQueue_t)dlsym(RTLD_NEXT,"hsaKmtUpdateQueue");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtDestroyQueue_fn) hsaKmtDestroyQueue_t;
  HSAKMTAPI_table->hsaKmtDestroyQueue_fn = (hsaKmtDestroyQueue_t)dlsym(RTLD_NEXT,"hsaKmtDestroyQueue");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSetQueueCUMask_fn) hsaKmtSetQueueCUMask_t;
  HSAKMTAPI_table->hsaKmtSetQueueCUMask_fn = (hsaKmtSetQueueCUMask_t)dlsym(RTLD_NEXT,"hsaKmtSetQueueCUMask");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetQueueInfo_fn) hsaKmtGetQueueInfo_t;
  HSAKMTAPI_table->hsaKmtGetQueueInfo_fn = (hsaKmtGetQueueInfo_t)dlsym(RTLD_NEXT,"hsaKmtGetQueueInfo");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSetMemoryPolicy_fn) hsaKmtSetMemoryPolicy_t;
  HSAKMTAPI_table->hsaKmtSetMemoryPolicy_fn = (hsaKmtSetMemoryPolicy_t)dlsym(RTLD_NEXT,"hsaKmtSetMemoryPolicy");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtAllocMemory_fn) hsaKmtAllocMemory_t;
  HSAKMTAPI_table->hsaKmtAllocMemory_fn = (hsaKmtAllocMemory_t)dlsym(RTLD_NEXT,"hsaKmtAllocMemory");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtFreeMemory_fn) hsaKmtFreeMemory_t;
  HSAKMTAPI_table->hsaKmtFreeMemory_fn = (hsaKmtFreeMemory_t)dlsym(RTLD_NEXT,"hsaKmtFreeMemory");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtRegisterMemory_fn) hsaKmtRegisterMemory_t;
  HSAKMTAPI_table->hsaKmtRegisterMemory_fn = (hsaKmtRegisterMemory_t)dlsym(RTLD_NEXT,"hsaKmtRegisterMemory");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtRegisterMemoryToNodes_fn) hsaKmtRegisterMemoryToNodes_t;
  HSAKMTAPI_table->hsaKmtRegisterMemoryToNodes_fn = (hsaKmtRegisterMemoryToNodes_t)dlsym(RTLD_NEXT,"hsaKmtRegisterMemoryToNodes");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtRegisterMemoryWithFlags_fn) hsaKmtRegisterMemoryWithFlags_t;
  HSAKMTAPI_table->hsaKmtRegisterMemoryWithFlags_fn = (hsaKmtRegisterMemoryWithFlags_t)dlsym(RTLD_NEXT,"hsaKmtRegisterMemoryWithFlags");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtRegisterGraphicsHandleToNodes_fn) hsaKmtRegisterGraphicsHandleToNodes_t;
  HSAKMTAPI_table->hsaKmtRegisterGraphicsHandleToNodes_fn = (hsaKmtRegisterGraphicsHandleToNodes_t)dlsym(RTLD_NEXT,"hsaKmtRegisterGraphicsHandleToNodes");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtShareMemory_fn) hsaKmtShareMemory_t;
  HSAKMTAPI_table->hsaKmtShareMemory_fn = (hsaKmtShareMemory_t)dlsym(RTLD_NEXT,"hsaKmtShareMemory");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtRegisterSharedHandle_fn) hsaKmtRegisterSharedHandle_t;
  HSAKMTAPI_table->hsaKmtRegisterSharedHandle_fn = (hsaKmtRegisterSharedHandle_t)dlsym(RTLD_NEXT,"hsaKmtRegisterSharedHandle");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtRegisterSharedHandleToNodes_fn) hsaKmtRegisterSharedHandleToNodes_t;
  HSAKMTAPI_table->hsaKmtRegisterSharedHandleToNodes_fn = (hsaKmtRegisterSharedHandleToNodes_t)dlsym(RTLD_NEXT,"hsaKmtRegisterSharedHandleToNodes");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtProcessVMRead_fn) hsaKmtProcessVMRead_t;
  HSAKMTAPI_table->hsaKmtProcessVMRead_fn = (hsaKmtProcessVMRead_t)dlsym(RTLD_NEXT,"hsaKmtProcessVMRead");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtProcessVMWrite_fn) hsaKmtProcessVMWrite_t;
  HSAKMTAPI_table->hsaKmtProcessVMWrite_fn = (hsaKmtProcessVMWrite_t)dlsym(RTLD_NEXT,"hsaKmtProcessVMWrite");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtDeregisterMemory_fn) hsaKmtDeregisterMemory_t;
  HSAKMTAPI_table->hsaKmtDeregisterMemory_fn = (hsaKmtDeregisterMemory_t)dlsym(RTLD_NEXT,"hsaKmtDeregisterMemory");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtMapMemoryToGPU_fn) hsaKmtMapMemoryToGPU_t;
  HSAKMTAPI_table->hsaKmtMapMemoryToGPU_fn = (hsaKmtMapMemoryToGPU_t)dlsym(RTLD_NEXT,"hsaKmtMapMemoryToGPU");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtMapMemoryToGPUNodes_fn) hsaKmtMapMemoryToGPUNodes_t;
  HSAKMTAPI_table->hsaKmtMapMemoryToGPUNodes_fn = (hsaKmtMapMemoryToGPUNodes_t)dlsym(RTLD_NEXT,"hsaKmtMapMemoryToGPUNodes");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtUnmapMemoryToGPU_fn) hsaKmtUnmapMemoryToGPU_t;
  HSAKMTAPI_table->hsaKmtUnmapMemoryToGPU_fn = (hsaKmtUnmapMemoryToGPU_t)dlsym(RTLD_NEXT,"hsaKmtUnmapMemoryToGPU");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtMapGraphicHandle_fn) hsaKmtMapGraphicHandle_t;
  HSAKMTAPI_table->hsaKmtMapGraphicHandle_fn = (hsaKmtMapGraphicHandle_t)dlsym(RTLD_NEXT,"hsaKmtMapGraphicHandle");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtUnmapGraphicHandle_fn) hsaKmtUnmapGraphicHandle_t;
  HSAKMTAPI_table->hsaKmtUnmapGraphicHandle_fn = (hsaKmtUnmapGraphicHandle_t)dlsym(RTLD_NEXT,"hsaKmtUnmapGraphicHandle");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtAllocQueueGWS_fn) hsaKmtAllocQueueGWS_t;
  HSAKMTAPI_table->hsaKmtAllocQueueGWS_fn = (hsaKmtAllocQueueGWS_t)dlsym(RTLD_NEXT,"hsaKmtAllocQueueGWS");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtDbgRegister_fn) hsaKmtDbgRegister_t;
  HSAKMTAPI_table->hsaKmtDbgRegister_fn = (hsaKmtDbgRegister_t)dlsym(RTLD_NEXT,"hsaKmtDbgRegister");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtDbgUnregister_fn) hsaKmtDbgUnregister_t;
  HSAKMTAPI_table->hsaKmtDbgUnregister_fn = (hsaKmtDbgUnregister_t)dlsym(RTLD_NEXT,"hsaKmtDbgUnregister");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtDbgWavefrontControl_fn) hsaKmtDbgWavefrontControl_t;
  HSAKMTAPI_table->hsaKmtDbgWavefrontControl_fn = (hsaKmtDbgWavefrontControl_t)dlsym(RTLD_NEXT,"hsaKmtDbgWavefrontControl");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtDbgAddressWatch_fn) hsaKmtDbgAddressWatch_t;
  HSAKMTAPI_table->hsaKmtDbgAddressWatch_fn = (hsaKmtDbgAddressWatch_t)dlsym(RTLD_NEXT,"hsaKmtDbgAddressWatch");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtQueueSuspend_fn) hsaKmtQueueSuspend_t;
  HSAKMTAPI_table->hsaKmtQueueSuspend_fn = (hsaKmtQueueSuspend_t)dlsym(RTLD_NEXT,"hsaKmtQueueSuspend");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtQueueResume_fn) hsaKmtQueueResume_t;
  HSAKMTAPI_table->hsaKmtQueueResume_fn = (hsaKmtQueueResume_t)dlsym(RTLD_NEXT,"hsaKmtQueueResume");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtEnableDebugTrap_fn) hsaKmtEnableDebugTrap_t;
  HSAKMTAPI_table->hsaKmtEnableDebugTrap_fn = (hsaKmtEnableDebugTrap_t)dlsym(RTLD_NEXT,"hsaKmtEnableDebugTrap");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtEnableDebugTrapWithPollFd_fn) hsaKmtEnableDebugTrapWithPollFd_t;
  HSAKMTAPI_table->hsaKmtEnableDebugTrapWithPollFd_fn = (hsaKmtEnableDebugTrapWithPollFd_t)dlsym(RTLD_NEXT,"hsaKmtEnableDebugTrapWithPollFd");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtDisableDebugTrap_fn) hsaKmtDisableDebugTrap_t;
  HSAKMTAPI_table->hsaKmtDisableDebugTrap_fn = (hsaKmtDisableDebugTrap_t)dlsym(RTLD_NEXT,"hsaKmtDisableDebugTrap");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtQueryDebugEvent_fn) hsaKmtQueryDebugEvent_t;
  HSAKMTAPI_table->hsaKmtQueryDebugEvent_fn = (hsaKmtQueryDebugEvent_t)dlsym(RTLD_NEXT,"hsaKmtQueryDebugEvent");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetQueueSnapshot_fn) hsaKmtGetQueueSnapshot_t;
  HSAKMTAPI_table->hsaKmtGetQueueSnapshot_fn = (hsaKmtGetQueueSnapshot_t)dlsym(RTLD_NEXT,"hsaKmtGetQueueSnapshot");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSendHostTrap_fn) hsaKmtSendHostTrap_t;
  HSAKMTAPI_table->hsaKmtSendHostTrap_fn = (hsaKmtSendHostTrap_t)dlsym(RTLD_NEXT,"hsaKmtSendHostTrap");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSetWaveLaunchTrapOverride_fn) hsaKmtSetWaveLaunchTrapOverride_t;
  HSAKMTAPI_table->hsaKmtSetWaveLaunchTrapOverride_fn = (hsaKmtSetWaveLaunchTrapOverride_t)dlsym(RTLD_NEXT,"hsaKmtSetWaveLaunchTrapOverride");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSetWaveLaunchMode_fn) hsaKmtSetWaveLaunchMode_t;
  HSAKMTAPI_table->hsaKmtSetWaveLaunchMode_fn = (hsaKmtSetWaveLaunchMode_t)dlsym(RTLD_NEXT,"hsaKmtSetWaveLaunchMode");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetKernelDebugTrapVersionInfo_fn) hsaKmtGetKernelDebugTrapVersionInfo_t;
  HSAKMTAPI_table->hsaKmtGetKernelDebugTrapVersionInfo_fn = (hsaKmtGetKernelDebugTrapVersionInfo_t)dlsym(RTLD_NEXT,"hsaKmtGetKernelDebugTrapVersionInfo");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetThunkDebugTrapVersionInfo_fn) hsaKmtGetThunkDebugTrapVersionInfo_t;
  HSAKMTAPI_table->hsaKmtGetThunkDebugTrapVersionInfo_fn = (hsaKmtGetThunkDebugTrapVersionInfo_t)dlsym(RTLD_NEXT,"hsaKmtGetThunkDebugTrapVersionInfo");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSetAddressWatch_fn) hsaKmtSetAddressWatch_t;
  HSAKMTAPI_table->hsaKmtSetAddressWatch_fn = (hsaKmtSetAddressWatch_t)dlsym(RTLD_NEXT,"hsaKmtSetAddressWatch");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtClearAddressWatch_fn) hsaKmtClearAddressWatch_t;
  HSAKMTAPI_table->hsaKmtClearAddressWatch_fn = (hsaKmtClearAddressWatch_t)dlsym(RTLD_NEXT,"hsaKmtClearAddressWatch");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtEnablePreciseMemoryOperations_fn) hsaKmtEnablePreciseMemoryOperations_t;
  HSAKMTAPI_table->hsaKmtEnablePreciseMemoryOperations_fn = (hsaKmtEnablePreciseMemoryOperations_t)dlsym(RTLD_NEXT,"hsaKmtEnablePreciseMemoryOperations");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtDisablePreciseMemoryOperations_fn) hsaKmtDisablePreciseMemoryOperations_t;
  HSAKMTAPI_table->hsaKmtDisablePreciseMemoryOperations_fn = (hsaKmtDisablePreciseMemoryOperations_t)dlsym(RTLD_NEXT,"hsaKmtDisablePreciseMemoryOperations");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetClockCounters_fn) hsaKmtGetClockCounters_t;
  HSAKMTAPI_table->hsaKmtGetClockCounters_fn = (hsaKmtGetClockCounters_t)dlsym(RTLD_NEXT,"hsaKmtGetClockCounters");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtPmcGetCounterProperties_fn) hsaKmtPmcGetCounterProperties_t;
  HSAKMTAPI_table->hsaKmtPmcGetCounterProperties_fn = (hsaKmtPmcGetCounterProperties_t)dlsym(RTLD_NEXT,"hsaKmtPmcGetCounterProperties");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtPmcRegisterTrace_fn) hsaKmtPmcRegisterTrace_t;
  HSAKMTAPI_table->hsaKmtPmcRegisterTrace_fn = (hsaKmtPmcRegisterTrace_t)dlsym(RTLD_NEXT,"hsaKmtPmcRegisterTrace");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtPmcUnregisterTrace_fn) hsaKmtPmcUnregisterTrace_t;
  HSAKMTAPI_table->hsaKmtPmcUnregisterTrace_fn = (hsaKmtPmcUnregisterTrace_t)dlsym(RTLD_NEXT,"hsaKmtPmcUnregisterTrace");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtPmcAcquireTraceAccess_fn) hsaKmtPmcAcquireTraceAccess_t;
  HSAKMTAPI_table->hsaKmtPmcAcquireTraceAccess_fn = (hsaKmtPmcAcquireTraceAccess_t)dlsym(RTLD_NEXT,"hsaKmtPmcAcquireTraceAccess");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtPmcReleaseTraceAccess_fn) hsaKmtPmcReleaseTraceAccess_t;
  HSAKMTAPI_table->hsaKmtPmcReleaseTraceAccess_fn = (hsaKmtPmcReleaseTraceAccess_t)dlsym(RTLD_NEXT,"hsaKmtPmcReleaseTraceAccess");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtPmcStartTrace_fn) hsaKmtPmcStartTrace_t;
  HSAKMTAPI_table->hsaKmtPmcStartTrace_fn = (hsaKmtPmcStartTrace_t)dlsym(RTLD_NEXT,"hsaKmtPmcStartTrace");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtPmcQueryTrace_fn) hsaKmtPmcQueryTrace_t;
  HSAKMTAPI_table->hsaKmtPmcQueryTrace_fn = (hsaKmtPmcQueryTrace_t)dlsym(RTLD_NEXT,"hsaKmtPmcQueryTrace");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtPmcStopTrace_fn) hsaKmtPmcStopTrace_t;
  HSAKMTAPI_table->hsaKmtPmcStopTrace_fn = (hsaKmtPmcStopTrace_t)dlsym(RTLD_NEXT,"hsaKmtPmcStopTrace");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSetTrapHandler_fn) hsaKmtSetTrapHandler_t;
  HSAKMTAPI_table->hsaKmtSetTrapHandler_fn = (hsaKmtSetTrapHandler_t)dlsym(RTLD_NEXT,"hsaKmtSetTrapHandler");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetTileConfig_fn) hsaKmtGetTileConfig_t;
  HSAKMTAPI_table->hsaKmtGetTileConfig_fn = (hsaKmtGetTileConfig_t)dlsym(RTLD_NEXT,"hsaKmtGetTileConfig");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtQueryPointerInfo_fn) hsaKmtQueryPointerInfo_t;
  HSAKMTAPI_table->hsaKmtQueryPointerInfo_fn = (hsaKmtQueryPointerInfo_t)dlsym(RTLD_NEXT,"hsaKmtQueryPointerInfo");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSetMemoryUserData_fn) hsaKmtSetMemoryUserData_t;
  HSAKMTAPI_table->hsaKmtSetMemoryUserData_fn = (hsaKmtSetMemoryUserData_t)dlsym(RTLD_NEXT,"hsaKmtSetMemoryUserData");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSPMAcquire_fn) hsaKmtSPMAcquire_t;
  HSAKMTAPI_table->hsaKmtSPMAcquire_fn = (hsaKmtSPMAcquire_t)dlsym(RTLD_NEXT,"hsaKmtSPMAcquire");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSPMRelease_fn) hsaKmtSPMRelease_t;
  HSAKMTAPI_table->hsaKmtSPMRelease_fn = (hsaKmtSPMRelease_t)dlsym(RTLD_NEXT,"hsaKmtSPMRelease");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSPMSetDestBuffer_fn) hsaKmtSPMSetDestBuffer_t;
  HSAKMTAPI_table->hsaKmtSPMSetDestBuffer_fn = (hsaKmtSPMSetDestBuffer_t)dlsym(RTLD_NEXT,"hsaKmtSPMSetDestBuffer");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSVMSetAttr_fn) hsaKmtSVMSetAttr_t;
  HSAKMTAPI_table->hsaKmtSVMSetAttr_fn = (hsaKmtSVMSetAttr_t)dlsym(RTLD_NEXT,"hsaKmtSVMSetAttr");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSVMGetAttr_fn) hsaKmtSVMGetAttr_t;
  HSAKMTAPI_table->hsaKmtSVMGetAttr_fn = (hsaKmtSVMGetAttr_t)dlsym(RTLD_NEXT,"hsaKmtSVMGetAttr");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtSetXNACKMode_fn) hsaKmtSetXNACKMode_t;
  HSAKMTAPI_table->hsaKmtSetXNACKMode_fn = (hsaKmtSetXNACKMode_t)dlsym(RTLD_NEXT,"hsaKmtSetXNACKMode");
  typedef decltype(HSAKMTAPI_table_t::hsaKmtGetXNACKMode_fn) hsaKmtGetXNACKMode_t;
  HSAKMTAPI_table->hsaKmtGetXNACKMode_fn = (hsaKmtGetXNACKMode_t)dlsym(RTLD_NEXT,"hsaKmtGetXNACKMode");
};

// section: API callback functions

typedef CbTable<KFD_API_ID_NUMBER> cb_table_t;
cb_table_t cb_table;

// block: HSAKMTAPI API
HSAKMT_STATUS hsaKmtOpenKFD_callback(void) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtOpenKFD, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtOpenKFD, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtOpenKFD_fn();
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtOpenKFD, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtCloseKFD_callback(void) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtCloseKFD, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtCloseKFD, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtCloseKFD_fn();
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtCloseKFD, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetVersion_callback(HsaVersionInfo* VersionInfo) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetVersion.VersionInfo = VersionInfo;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetVersion, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetVersion, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetVersion_fn(VersionInfo);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetVersion, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtAcquireSystemProperties_callback(HsaSystemProperties* SystemProperties) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtAcquireSystemProperties.SystemProperties = SystemProperties;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtAcquireSystemProperties, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtAcquireSystemProperties, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtAcquireSystemProperties_fn(SystemProperties);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtAcquireSystemProperties, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtReleaseSystemProperties_callback(void) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtReleaseSystemProperties, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtReleaseSystemProperties, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtReleaseSystemProperties_fn();
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtReleaseSystemProperties, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetNodeProperties_callback(HSAuint32               NodeId, HsaNodeProperties* NodeProperties) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetNodeProperties.NodeId = NodeId;
  api_data.args.hsaKmtGetNodeProperties.NodeProperties = NodeProperties;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetNodeProperties, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetNodeProperties, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetNodeProperties_fn(NodeId, NodeProperties);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetNodeProperties, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetNodeMemoryProperties_callback(HSAuint32             NodeId, HSAuint32             NumBanks, HsaMemoryProperties* MemoryProperties) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetNodeMemoryProperties.NodeId = NodeId;
  api_data.args.hsaKmtGetNodeMemoryProperties.NumBanks = NumBanks;
  api_data.args.hsaKmtGetNodeMemoryProperties.MemoryProperties = MemoryProperties;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetNodeMemoryProperties, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetNodeMemoryProperties, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetNodeMemoryProperties_fn(NodeId, NumBanks, MemoryProperties);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetNodeMemoryProperties, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetNodeCacheProperties_callback(HSAuint32           NodeId, HSAuint32           ProcessorId, HSAuint32           NumCaches, HsaCacheProperties* CacheProperties) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetNodeCacheProperties.NodeId = NodeId;
  api_data.args.hsaKmtGetNodeCacheProperties.ProcessorId = ProcessorId;
  api_data.args.hsaKmtGetNodeCacheProperties.NumCaches = NumCaches;
  api_data.args.hsaKmtGetNodeCacheProperties.CacheProperties = CacheProperties;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetNodeCacheProperties, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetNodeCacheProperties, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetNodeCacheProperties_fn(NodeId, ProcessorId, NumCaches, CacheProperties);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetNodeCacheProperties, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetNodeIoLinkProperties_callback(HSAuint32            NodeId, HSAuint32            NumIoLinks, HsaIoLinkProperties* IoLinkProperties) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetNodeIoLinkProperties.NodeId = NodeId;
  api_data.args.hsaKmtGetNodeIoLinkProperties.NumIoLinks = NumIoLinks;
  api_data.args.hsaKmtGetNodeIoLinkProperties.IoLinkProperties = IoLinkProperties;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetNodeIoLinkProperties, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetNodeIoLinkProperties, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetNodeIoLinkProperties_fn(NodeId, NumIoLinks, IoLinkProperties);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetNodeIoLinkProperties, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtCreateEvent_callback(HsaEventDescriptor* EventDesc, bool                ManualReset, bool                IsSignaled, HsaEvent** Event) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtCreateEvent.EventDesc = EventDesc;
  api_data.args.hsaKmtCreateEvent.ManualReset = ManualReset;
  api_data.args.hsaKmtCreateEvent.IsSignaled = IsSignaled;
  api_data.args.hsaKmtCreateEvent.Event = Event;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtCreateEvent, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtCreateEvent, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtCreateEvent_fn(EventDesc, ManualReset, IsSignaled, Event);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtCreateEvent, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtDestroyEvent_callback(HsaEvent* Event) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtDestroyEvent.Event = Event;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtDestroyEvent, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDestroyEvent, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtDestroyEvent_fn(Event);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDestroyEvent, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSetEvent_callback(HsaEvent* Event) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSetEvent.Event = Event;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSetEvent, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetEvent, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSetEvent_fn(Event);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetEvent, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtResetEvent_callback(HsaEvent* Event) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtResetEvent.Event = Event;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtResetEvent, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtResetEvent, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtResetEvent_fn(Event);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtResetEvent, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtQueryEventState_callback(HsaEvent* Event) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtQueryEventState.Event = Event;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtQueryEventState, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtQueryEventState, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtQueryEventState_fn(Event);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtQueryEventState, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtWaitOnEvent_callback(HsaEvent* Event, HSAuint32   Milliseconds) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtWaitOnEvent.Event = Event;
  api_data.args.hsaKmtWaitOnEvent.Milliseconds = Milliseconds;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtWaitOnEvent, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtWaitOnEvent, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtWaitOnEvent_fn(Event, Milliseconds);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtWaitOnEvent, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtWaitOnMultipleEvents_callback(HsaEvent* Events[], HSAuint32   NumEvents, bool        WaitOnAll, HSAuint32   Milliseconds) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtWaitOnMultipleEvents.Events = Events;
  api_data.args.hsaKmtWaitOnMultipleEvents.NumEvents = NumEvents;
  api_data.args.hsaKmtWaitOnMultipleEvents.WaitOnAll = WaitOnAll;
  api_data.args.hsaKmtWaitOnMultipleEvents.Milliseconds = Milliseconds;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtWaitOnMultipleEvents, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtWaitOnMultipleEvents, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtWaitOnMultipleEvents_fn(Events, NumEvents, WaitOnAll, Milliseconds);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtWaitOnMultipleEvents, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtReportQueue_callback(HSA_QUEUEID     QueueId, HsaQueueReport* QueueReport) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtReportQueue.QueueId = QueueId;
  api_data.args.hsaKmtReportQueue.QueueReport = QueueReport;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtReportQueue, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtReportQueue, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtReportQueue_fn(QueueId, QueueReport);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtReportQueue, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtCreateQueue_callback(HSAuint32           NodeId, HSA_QUEUE_TYPE      Type, HSAuint32           QueuePercentage, HSA_QUEUE_PRIORITY  Priority, void* QueueAddress, HSAuint64           QueueSizeInBytes, HsaEvent* Event, HsaQueueResource* QueueResource) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtCreateQueue.NodeId = NodeId;
  api_data.args.hsaKmtCreateQueue.Type = Type;
  api_data.args.hsaKmtCreateQueue.QueuePercentage = QueuePercentage;
  api_data.args.hsaKmtCreateQueue.Priority = Priority;
  api_data.args.hsaKmtCreateQueue.QueueAddress = QueueAddress;
  api_data.args.hsaKmtCreateQueue.QueueSizeInBytes = QueueSizeInBytes;
  api_data.args.hsaKmtCreateQueue.Event = Event;
  api_data.args.hsaKmtCreateQueue.QueueResource = QueueResource;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtCreateQueue, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtCreateQueue, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtCreateQueue_fn(NodeId, Type, QueuePercentage, Priority, QueueAddress, QueueSizeInBytes, Event, QueueResource);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtCreateQueue, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtUpdateQueue_callback(HSA_QUEUEID         QueueId, HSAuint32           QueuePercentage, HSA_QUEUE_PRIORITY  Priority, void* QueueAddress, HSAuint64           QueueSize, HsaEvent* Event) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtUpdateQueue.QueueId = QueueId;
  api_data.args.hsaKmtUpdateQueue.QueuePercentage = QueuePercentage;
  api_data.args.hsaKmtUpdateQueue.Priority = Priority;
  api_data.args.hsaKmtUpdateQueue.QueueAddress = QueueAddress;
  api_data.args.hsaKmtUpdateQueue.QueueSize = QueueSize;
  api_data.args.hsaKmtUpdateQueue.Event = Event;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtUpdateQueue, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtUpdateQueue, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtUpdateQueue_fn(QueueId, QueuePercentage, Priority, QueueAddress, QueueSize, Event);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtUpdateQueue, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtDestroyQueue_callback(HSA_QUEUEID         QueueId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtDestroyQueue.QueueId = QueueId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtDestroyQueue, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDestroyQueue, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtDestroyQueue_fn(QueueId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDestroyQueue, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSetQueueCUMask_callback(HSA_QUEUEID         QueueId, HSAuint32           CUMaskCount, HSAuint32* QueueCUMask) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSetQueueCUMask.QueueId = QueueId;
  api_data.args.hsaKmtSetQueueCUMask.CUMaskCount = CUMaskCount;
  api_data.args.hsaKmtSetQueueCUMask.QueueCUMask = QueueCUMask;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSetQueueCUMask, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetQueueCUMask, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSetQueueCUMask_fn(QueueId, CUMaskCount, QueueCUMask);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetQueueCUMask, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetQueueInfo_callback(HSA_QUEUEID QueueId, HsaQueueInfo* QueueInfo) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetQueueInfo.QueueId = QueueId;
  api_data.args.hsaKmtGetQueueInfo.QueueInfo = QueueInfo;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetQueueInfo, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetQueueInfo, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetQueueInfo_fn(QueueId, QueueInfo);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetQueueInfo, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSetMemoryPolicy_callback(HSAuint32       Node, HSAuint32       DefaultPolicy, HSAuint32       AlternatePolicy, void* MemoryAddressAlternate, HSAuint64       MemorySizeInBytes) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSetMemoryPolicy.Node = Node;
  api_data.args.hsaKmtSetMemoryPolicy.DefaultPolicy = DefaultPolicy;
  api_data.args.hsaKmtSetMemoryPolicy.AlternatePolicy = AlternatePolicy;
  api_data.args.hsaKmtSetMemoryPolicy.MemoryAddressAlternate = MemoryAddressAlternate;
  api_data.args.hsaKmtSetMemoryPolicy.MemorySizeInBytes = MemorySizeInBytes;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSetMemoryPolicy, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetMemoryPolicy, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSetMemoryPolicy_fn(Node, DefaultPolicy, AlternatePolicy, MemoryAddressAlternate, MemorySizeInBytes);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetMemoryPolicy, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtAllocMemory_callback(HSAuint32       PreferredNode, HSAuint64       SizeInBytes, HsaMemFlags     MemFlags, void** MemoryAddress) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtAllocMemory.PreferredNode = PreferredNode;
  api_data.args.hsaKmtAllocMemory.SizeInBytes = SizeInBytes;
  api_data.args.hsaKmtAllocMemory.MemFlags = MemFlags;
  api_data.args.hsaKmtAllocMemory.MemoryAddress = MemoryAddress;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtAllocMemory, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtAllocMemory, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtAllocMemory_fn(PreferredNode, SizeInBytes, MemFlags, MemoryAddress);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtAllocMemory, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtFreeMemory_callback(void* MemoryAddress, HSAuint64   SizeInBytes) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtFreeMemory.MemoryAddress = MemoryAddress;
  api_data.args.hsaKmtFreeMemory.SizeInBytes = SizeInBytes;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtFreeMemory, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtFreeMemory, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtFreeMemory_fn(MemoryAddress, SizeInBytes);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtFreeMemory, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtRegisterMemory_callback(void* MemoryAddress, HSAuint64   MemorySizeInBytes) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtRegisterMemory.MemoryAddress = MemoryAddress;
  api_data.args.hsaKmtRegisterMemory.MemorySizeInBytes = MemorySizeInBytes;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtRegisterMemory, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterMemory, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtRegisterMemory_fn(MemoryAddress, MemorySizeInBytes);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterMemory, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtRegisterMemoryToNodes_callback(void* MemoryAddress, HSAuint64   MemorySizeInBytes, HSAuint64   NumberOfNodes, HSAuint32* NodeArray) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtRegisterMemoryToNodes.MemoryAddress = MemoryAddress;
  api_data.args.hsaKmtRegisterMemoryToNodes.MemorySizeInBytes = MemorySizeInBytes;
  api_data.args.hsaKmtRegisterMemoryToNodes.NumberOfNodes = NumberOfNodes;
  api_data.args.hsaKmtRegisterMemoryToNodes.NodeArray = NodeArray;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtRegisterMemoryToNodes, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterMemoryToNodes, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtRegisterMemoryToNodes_fn(MemoryAddress, MemorySizeInBytes, NumberOfNodes, NodeArray);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterMemoryToNodes, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtRegisterMemoryWithFlags_callback(void* MemoryAddress, HSAuint64   MemorySizeInBytes, HsaMemFlags MemFlags) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtRegisterMemoryWithFlags.MemoryAddress = MemoryAddress;
  api_data.args.hsaKmtRegisterMemoryWithFlags.MemorySizeInBytes = MemorySizeInBytes;
  api_data.args.hsaKmtRegisterMemoryWithFlags.MemFlags = MemFlags;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtRegisterMemoryWithFlags, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterMemoryWithFlags, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtRegisterMemoryWithFlags_fn(MemoryAddress, MemorySizeInBytes, MemFlags);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterMemoryWithFlags, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtRegisterGraphicsHandleToNodes_callback(HSAuint64       GraphicsResourceHandle, HsaGraphicsResourceInfo* GraphicsResourceInfo, HSAuint64       NumberOfNodes, HSAuint32* NodeArray) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtRegisterGraphicsHandleToNodes.GraphicsResourceHandle = GraphicsResourceHandle;
  api_data.args.hsaKmtRegisterGraphicsHandleToNodes.GraphicsResourceInfo = GraphicsResourceInfo;
  api_data.args.hsaKmtRegisterGraphicsHandleToNodes.NumberOfNodes = NumberOfNodes;
  api_data.args.hsaKmtRegisterGraphicsHandleToNodes.NodeArray = NodeArray;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtRegisterGraphicsHandleToNodes, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterGraphicsHandleToNodes, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtRegisterGraphicsHandleToNodes_fn(GraphicsResourceHandle, GraphicsResourceInfo, NumberOfNodes, NodeArray);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterGraphicsHandleToNodes, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtShareMemory_callback(void* MemoryAddress, HSAuint64             SizeInBytes, HsaSharedMemoryHandle* SharedMemoryHandle) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtShareMemory.MemoryAddress = MemoryAddress;
  api_data.args.hsaKmtShareMemory.SizeInBytes = SizeInBytes;
  api_data.args.hsaKmtShareMemory.SharedMemoryHandle = SharedMemoryHandle;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtShareMemory, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtShareMemory, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtShareMemory_fn(MemoryAddress, SizeInBytes, SharedMemoryHandle);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtShareMemory, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtRegisterSharedHandle_callback(const HsaSharedMemoryHandle* SharedMemoryHandle, void** MemoryAddress, HSAuint64* SizeInBytes) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtRegisterSharedHandle.SharedMemoryHandle = SharedMemoryHandle;
  api_data.args.hsaKmtRegisterSharedHandle.MemoryAddress = MemoryAddress;
  api_data.args.hsaKmtRegisterSharedHandle.SizeInBytes = SizeInBytes;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtRegisterSharedHandle, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterSharedHandle, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtRegisterSharedHandle_fn(SharedMemoryHandle, MemoryAddress, SizeInBytes);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterSharedHandle, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtRegisterSharedHandleToNodes_callback(const HsaSharedMemoryHandle* SharedMemoryHandle, void** MemoryAddress, HSAuint64* SizeInBytes, HSAuint64                   NumberOfNodes, HSAuint32* NodeArray) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtRegisterSharedHandleToNodes.SharedMemoryHandle = SharedMemoryHandle;
  api_data.args.hsaKmtRegisterSharedHandleToNodes.MemoryAddress = MemoryAddress;
  api_data.args.hsaKmtRegisterSharedHandleToNodes.SizeInBytes = SizeInBytes;
  api_data.args.hsaKmtRegisterSharedHandleToNodes.NumberOfNodes = NumberOfNodes;
  api_data.args.hsaKmtRegisterSharedHandleToNodes.NodeArray = NodeArray;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtRegisterSharedHandleToNodes, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterSharedHandleToNodes, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtRegisterSharedHandleToNodes_fn(SharedMemoryHandle, MemoryAddress, SizeInBytes, NumberOfNodes, NodeArray);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtRegisterSharedHandleToNodes, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtProcessVMRead_callback(HSAuint32                 Pid, HsaMemoryRange* LocalMemoryArray, HSAuint64                 LocalMemoryArrayCount, HsaMemoryRange* RemoteMemoryArray, HSAuint64                 RemoteMemoryArrayCount, HSAuint64* SizeCopied) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtProcessVMRead.Pid = Pid;
  api_data.args.hsaKmtProcessVMRead.LocalMemoryArray = LocalMemoryArray;
  api_data.args.hsaKmtProcessVMRead.LocalMemoryArrayCount = LocalMemoryArrayCount;
  api_data.args.hsaKmtProcessVMRead.RemoteMemoryArray = RemoteMemoryArray;
  api_data.args.hsaKmtProcessVMRead.RemoteMemoryArrayCount = RemoteMemoryArrayCount;
  api_data.args.hsaKmtProcessVMRead.SizeCopied = SizeCopied;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtProcessVMRead, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtProcessVMRead, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtProcessVMRead_fn(Pid, LocalMemoryArray, LocalMemoryArrayCount, RemoteMemoryArray, RemoteMemoryArrayCount, SizeCopied);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtProcessVMRead, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtProcessVMWrite_callback(HSAuint32                 Pid, HsaMemoryRange* LocalMemoryArray, HSAuint64                 LocalMemoryArrayCount, HsaMemoryRange* RemoteMemoryArray, HSAuint64                 RemoteMemoryArrayCount, HSAuint64* SizeCopied) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtProcessVMWrite.Pid = Pid;
  api_data.args.hsaKmtProcessVMWrite.LocalMemoryArray = LocalMemoryArray;
  api_data.args.hsaKmtProcessVMWrite.LocalMemoryArrayCount = LocalMemoryArrayCount;
  api_data.args.hsaKmtProcessVMWrite.RemoteMemoryArray = RemoteMemoryArray;
  api_data.args.hsaKmtProcessVMWrite.RemoteMemoryArrayCount = RemoteMemoryArrayCount;
  api_data.args.hsaKmtProcessVMWrite.SizeCopied = SizeCopied;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtProcessVMWrite, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtProcessVMWrite, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtProcessVMWrite_fn(Pid, LocalMemoryArray, LocalMemoryArrayCount, RemoteMemoryArray, RemoteMemoryArrayCount, SizeCopied);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtProcessVMWrite, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtDeregisterMemory_callback(void* MemoryAddress) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtDeregisterMemory.MemoryAddress = MemoryAddress;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtDeregisterMemory, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDeregisterMemory, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtDeregisterMemory_fn(MemoryAddress);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDeregisterMemory, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtMapMemoryToGPU_callback(void* MemoryAddress, HSAuint64       MemorySizeInBytes, HSAuint64* AlternateVAGPU) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtMapMemoryToGPU.MemoryAddress = MemoryAddress;
  api_data.args.hsaKmtMapMemoryToGPU.MemorySizeInBytes = MemorySizeInBytes;
  api_data.args.hsaKmtMapMemoryToGPU.AlternateVAGPU = AlternateVAGPU;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtMapMemoryToGPU, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtMapMemoryToGPU, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtMapMemoryToGPU_fn(MemoryAddress, MemorySizeInBytes, AlternateVAGPU);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtMapMemoryToGPU, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtMapMemoryToGPUNodes_callback(void* MemoryAddress, HSAuint64       MemorySizeInBytes, HSAuint64* AlternateVAGPU, HsaMemMapFlags  MemMapFlags, HSAuint64       NumberOfNodes, HSAuint32* NodeArray) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtMapMemoryToGPUNodes.MemoryAddress = MemoryAddress;
  api_data.args.hsaKmtMapMemoryToGPUNodes.MemorySizeInBytes = MemorySizeInBytes;
  api_data.args.hsaKmtMapMemoryToGPUNodes.AlternateVAGPU = AlternateVAGPU;
  api_data.args.hsaKmtMapMemoryToGPUNodes.MemMapFlags = MemMapFlags;
  api_data.args.hsaKmtMapMemoryToGPUNodes.NumberOfNodes = NumberOfNodes;
  api_data.args.hsaKmtMapMemoryToGPUNodes.NodeArray = NodeArray;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtMapMemoryToGPUNodes, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtMapMemoryToGPUNodes, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtMapMemoryToGPUNodes_fn(MemoryAddress, MemorySizeInBytes, AlternateVAGPU, MemMapFlags, NumberOfNodes, NodeArray);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtMapMemoryToGPUNodes, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtUnmapMemoryToGPU_callback(void* MemoryAddress) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtUnmapMemoryToGPU.MemoryAddress = MemoryAddress;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtUnmapMemoryToGPU, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtUnmapMemoryToGPU, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtUnmapMemoryToGPU_fn(MemoryAddress);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtUnmapMemoryToGPU, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtMapGraphicHandle_callback(HSAuint32          NodeId, HSAuint64          GraphicDeviceHandle, HSAuint64          GraphicResourceHandle, HSAuint64          GraphicResourceOffset, HSAuint64          GraphicResourceSize, HSAuint64* FlatMemoryAddress) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtMapGraphicHandle.NodeId = NodeId;
  api_data.args.hsaKmtMapGraphicHandle.GraphicDeviceHandle = GraphicDeviceHandle;
  api_data.args.hsaKmtMapGraphicHandle.GraphicResourceHandle = GraphicResourceHandle;
  api_data.args.hsaKmtMapGraphicHandle.GraphicResourceOffset = GraphicResourceOffset;
  api_data.args.hsaKmtMapGraphicHandle.GraphicResourceSize = GraphicResourceSize;
  api_data.args.hsaKmtMapGraphicHandle.FlatMemoryAddress = FlatMemoryAddress;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtMapGraphicHandle, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtMapGraphicHandle, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtMapGraphicHandle_fn(NodeId, GraphicDeviceHandle, GraphicResourceHandle, GraphicResourceOffset, GraphicResourceSize, FlatMemoryAddress);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtMapGraphicHandle, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtUnmapGraphicHandle_callback(HSAuint32          NodeId, HSAuint64          FlatMemoryAddress, HSAuint64              SizeInBytes) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtUnmapGraphicHandle.NodeId = NodeId;
  api_data.args.hsaKmtUnmapGraphicHandle.FlatMemoryAddress = FlatMemoryAddress;
  api_data.args.hsaKmtUnmapGraphicHandle.SizeInBytes = SizeInBytes;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtUnmapGraphicHandle, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtUnmapGraphicHandle, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtUnmapGraphicHandle_fn(NodeId, FlatMemoryAddress, SizeInBytes);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtUnmapGraphicHandle, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtAllocQueueGWS_callback(HSA_QUEUEID        QueueId, HSAuint32          nGWS, HSAuint32* firstGWS) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtAllocQueueGWS.QueueId = QueueId;
  api_data.args.hsaKmtAllocQueueGWS.nGWS = nGWS;
  api_data.args.hsaKmtAllocQueueGWS.firstGWS = firstGWS;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtAllocQueueGWS, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtAllocQueueGWS, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtAllocQueueGWS_fn(QueueId, nGWS, firstGWS);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtAllocQueueGWS, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtDbgRegister_callback(HSAuint32       NodeId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtDbgRegister.NodeId = NodeId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtDbgRegister, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDbgRegister, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtDbgRegister_fn(NodeId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDbgRegister, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtDbgUnregister_callback(HSAuint32       NodeId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtDbgUnregister.NodeId = NodeId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtDbgUnregister, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDbgUnregister, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtDbgUnregister_fn(NodeId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDbgUnregister, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtDbgWavefrontControl_callback(HSAuint32           NodeId, HSA_DBG_WAVEOP      Operand, HSA_DBG_WAVEMODE    Mode, HSAuint32           TrapId, HsaDbgWaveMessage* DbgWaveMsgRing) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtDbgWavefrontControl.NodeId = NodeId;
  api_data.args.hsaKmtDbgWavefrontControl.Operand = Operand;
  api_data.args.hsaKmtDbgWavefrontControl.Mode = Mode;
  api_data.args.hsaKmtDbgWavefrontControl.TrapId = TrapId;
  api_data.args.hsaKmtDbgWavefrontControl.DbgWaveMsgRing = DbgWaveMsgRing;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtDbgWavefrontControl, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDbgWavefrontControl, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtDbgWavefrontControl_fn(NodeId, Operand, Mode, TrapId, DbgWaveMsgRing);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDbgWavefrontControl, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtDbgAddressWatch_callback(HSAuint32           NodeId, HSAuint32           NumWatchPoints, HSA_DBG_WATCH_MODE  WatchMode[], void* WatchAddress[], HSAuint64           WatchMask[], HsaEvent* WatchEvent[]) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtDbgAddressWatch.NodeId = NodeId;
  api_data.args.hsaKmtDbgAddressWatch.NumWatchPoints = NumWatchPoints;
  api_data.args.hsaKmtDbgAddressWatch.WatchMode = WatchMode;
  api_data.args.hsaKmtDbgAddressWatch.WatchAddress = WatchAddress;
  api_data.args.hsaKmtDbgAddressWatch.WatchMask = WatchMask;
  api_data.args.hsaKmtDbgAddressWatch.WatchEvent = WatchEvent;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtDbgAddressWatch, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDbgAddressWatch, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtDbgAddressWatch_fn(NodeId, NumWatchPoints, WatchMode, WatchAddress, WatchMask, WatchEvent);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDbgAddressWatch, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtQueueSuspend_callback(HSAuint32    Pid, HSAuint32    NumQueues, HSA_QUEUEID* Queues, HSAuint32    GracePeriod, HSAuint32    Flags) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtQueueSuspend.Pid = Pid;
  api_data.args.hsaKmtQueueSuspend.NumQueues = NumQueues;
  api_data.args.hsaKmtQueueSuspend.Queues = Queues;
  api_data.args.hsaKmtQueueSuspend.GracePeriod = GracePeriod;
  api_data.args.hsaKmtQueueSuspend.Flags = Flags;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtQueueSuspend, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtQueueSuspend, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtQueueSuspend_fn(Pid, NumQueues, Queues, GracePeriod, Flags);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtQueueSuspend, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtQueueResume_callback(HSAuint32   Pid, HSAuint32   NumQueues, HSA_QUEUEID* Queues, HSAuint32   Flags) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtQueueResume.Pid = Pid;
  api_data.args.hsaKmtQueueResume.NumQueues = NumQueues;
  api_data.args.hsaKmtQueueResume.Queues = Queues;
  api_data.args.hsaKmtQueueResume.Flags = Flags;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtQueueResume, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtQueueResume, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtQueueResume_fn(Pid, NumQueues, Queues, Flags);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtQueueResume, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtEnableDebugTrap_callback(HSAuint32	NodeId, HSA_QUEUEID	QueueId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtEnableDebugTrap.NodeId = NodeId;
  api_data.args.hsaKmtEnableDebugTrap.QueueId = QueueId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtEnableDebugTrap, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtEnableDebugTrap, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtEnableDebugTrap_fn(NodeId, QueueId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtEnableDebugTrap, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtEnableDebugTrapWithPollFd_callback(HSAuint32	NodeId, HSA_QUEUEID	QueueId, HSAint32* PollFd) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtEnableDebugTrapWithPollFd.NodeId = NodeId;
  api_data.args.hsaKmtEnableDebugTrapWithPollFd.QueueId = QueueId;
  api_data.args.hsaKmtEnableDebugTrapWithPollFd.PollFd = PollFd;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtEnableDebugTrapWithPollFd, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtEnableDebugTrapWithPollFd, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtEnableDebugTrapWithPollFd_fn(NodeId, QueueId, PollFd);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtEnableDebugTrapWithPollFd, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtDisableDebugTrap_callback(HSAuint32 NodeId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtDisableDebugTrap.NodeId = NodeId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtDisableDebugTrap, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDisableDebugTrap, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtDisableDebugTrap_fn(NodeId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDisableDebugTrap, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtQueryDebugEvent_callback(HSAuint32			NodeId, HSAuint32			Pid, HSAuint32* QueueId, bool			ClearEvents, HSA_DEBUG_EVENT_TYPE* EventsReceived, bool* IsSuspended, bool* IsNew) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtQueryDebugEvent.NodeId = NodeId;
  api_data.args.hsaKmtQueryDebugEvent.Pid = Pid;
  api_data.args.hsaKmtQueryDebugEvent.QueueId = QueueId;
  api_data.args.hsaKmtQueryDebugEvent.ClearEvents = ClearEvents;
  api_data.args.hsaKmtQueryDebugEvent.EventsReceived = EventsReceived;
  api_data.args.hsaKmtQueryDebugEvent.IsSuspended = IsSuspended;
  api_data.args.hsaKmtQueryDebugEvent.IsNew = IsNew;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtQueryDebugEvent, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtQueryDebugEvent, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtQueryDebugEvent_fn(NodeId, Pid, QueueId, ClearEvents, EventsReceived, IsSuspended, IsNew);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtQueryDebugEvent, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetQueueSnapshot_callback(HSAuint32			NodeId, HSAuint32			Pid, bool			ClearEvents, void* SnapshotBuf, HSAuint32* QssEntries) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetQueueSnapshot.NodeId = NodeId;
  api_data.args.hsaKmtGetQueueSnapshot.Pid = Pid;
  api_data.args.hsaKmtGetQueueSnapshot.ClearEvents = ClearEvents;
  api_data.args.hsaKmtGetQueueSnapshot.SnapshotBuf = SnapshotBuf;
  api_data.args.hsaKmtGetQueueSnapshot.QssEntries = QssEntries;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetQueueSnapshot, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetQueueSnapshot, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetQueueSnapshot_fn(NodeId, Pid, ClearEvents, SnapshotBuf, QssEntries);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetQueueSnapshot, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSendHostTrap_callback(HSAuint32	NodeId, HSAuint32	Pid) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSendHostTrap.NodeId = NodeId;
  api_data.args.hsaKmtSendHostTrap.Pid = Pid;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSendHostTrap, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSendHostTrap, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSendHostTrap_fn(NodeId, Pid);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSendHostTrap, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSetWaveLaunchTrapOverride_callback(HSAuint32             NodeId, HSA_DBG_TRAP_OVERRIDE TrapOverride, HSA_DBG_TRAP_MASK     TrapMask) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSetWaveLaunchTrapOverride.NodeId = NodeId;
  api_data.args.hsaKmtSetWaveLaunchTrapOverride.TrapOverride = TrapOverride;
  api_data.args.hsaKmtSetWaveLaunchTrapOverride.TrapMask = TrapMask;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSetWaveLaunchTrapOverride, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetWaveLaunchTrapOverride, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSetWaveLaunchTrapOverride_fn(NodeId, TrapOverride, TrapMask);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetWaveLaunchTrapOverride, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSetWaveLaunchMode_callback(HSAuint32                NodeId, HSA_DBG_WAVE_LAUNCH_MODE WaveLaunchMode) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSetWaveLaunchMode.NodeId = NodeId;
  api_data.args.hsaKmtSetWaveLaunchMode.WaveLaunchMode = WaveLaunchMode;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSetWaveLaunchMode, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetWaveLaunchMode, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSetWaveLaunchMode_fn(NodeId, WaveLaunchMode);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetWaveLaunchMode, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetKernelDebugTrapVersionInfo_callback(HSAuint32* Major, HSAuint32* Minor) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetKernelDebugTrapVersionInfo.Major = Major;
  api_data.args.hsaKmtGetKernelDebugTrapVersionInfo.Minor = Minor;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetKernelDebugTrapVersionInfo, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetKernelDebugTrapVersionInfo, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetKernelDebugTrapVersionInfo_fn(Major, Minor);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetKernelDebugTrapVersionInfo, &api_data, api_callback_arg);
  return ret;
}
void hsaKmtGetThunkDebugTrapVersionInfo_callback(HSAuint32* Major, HSAuint32* Minor) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetThunkDebugTrapVersionInfo.Major = Major;
  api_data.args.hsaKmtGetThunkDebugTrapVersionInfo.Minor = Minor;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetThunkDebugTrapVersionInfo, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetThunkDebugTrapVersionInfo, &api_data, api_callback_arg);
  HSAKMTAPI_table->hsaKmtGetThunkDebugTrapVersionInfo_fn(Major, Minor);
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetThunkDebugTrapVersionInfo, &api_data, api_callback_arg);
}
HSAKMT_STATUS hsaKmtSetAddressWatch_callback(HSAuint32          NodeId, HSAuint32          Pid, HSA_DBG_WATCH_MODE WatchMode, void* WatchAddress, HSAuint64          WatchAddrMask, HSAuint32* WatchId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSetAddressWatch.NodeId = NodeId;
  api_data.args.hsaKmtSetAddressWatch.Pid = Pid;
  api_data.args.hsaKmtSetAddressWatch.WatchMode = WatchMode;
  api_data.args.hsaKmtSetAddressWatch.WatchAddress = WatchAddress;
  api_data.args.hsaKmtSetAddressWatch.WatchAddrMask = WatchAddrMask;
  api_data.args.hsaKmtSetAddressWatch.WatchId = WatchId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSetAddressWatch, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetAddressWatch, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSetAddressWatch_fn(NodeId, Pid, WatchMode, WatchAddress, WatchAddrMask, WatchId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetAddressWatch, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtClearAddressWatch_callback(HSAuint32 NodeId, HSAuint32 Pid, HSAuint32 WatchId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtClearAddressWatch.NodeId = NodeId;
  api_data.args.hsaKmtClearAddressWatch.Pid = Pid;
  api_data.args.hsaKmtClearAddressWatch.WatchId = WatchId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtClearAddressWatch, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtClearAddressWatch, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtClearAddressWatch_fn(NodeId, Pid, WatchId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtClearAddressWatch, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtEnablePreciseMemoryOperations_callback(HSAuint32 NodeId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtEnablePreciseMemoryOperations.NodeId = NodeId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtEnablePreciseMemoryOperations, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtEnablePreciseMemoryOperations, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtEnablePreciseMemoryOperations_fn(NodeId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtEnablePreciseMemoryOperations, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtDisablePreciseMemoryOperations_callback(HSAuint32 NodeId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtDisablePreciseMemoryOperations.NodeId = NodeId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtDisablePreciseMemoryOperations, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDisablePreciseMemoryOperations, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtDisablePreciseMemoryOperations_fn(NodeId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtDisablePreciseMemoryOperations, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetClockCounters_callback(HSAuint32         NodeId, HsaClockCounters* Counters) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetClockCounters.NodeId = NodeId;
  api_data.args.hsaKmtGetClockCounters.Counters = Counters;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetClockCounters, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetClockCounters, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetClockCounters_fn(NodeId, Counters);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetClockCounters, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtPmcGetCounterProperties_callback(HSAuint32                   NodeId, HsaCounterProperties** CounterProperties) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtPmcGetCounterProperties.NodeId = NodeId;
  api_data.args.hsaKmtPmcGetCounterProperties.CounterProperties = CounterProperties;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtPmcGetCounterProperties, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcGetCounterProperties, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtPmcGetCounterProperties_fn(NodeId, CounterProperties);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcGetCounterProperties, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtPmcRegisterTrace_callback(HSAuint32           NodeId, HSAuint32           NumberOfCounters, HsaCounter* Counters, HsaPmcTraceRoot* TraceRoot) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtPmcRegisterTrace.NodeId = NodeId;
  api_data.args.hsaKmtPmcRegisterTrace.NumberOfCounters = NumberOfCounters;
  api_data.args.hsaKmtPmcRegisterTrace.Counters = Counters;
  api_data.args.hsaKmtPmcRegisterTrace.TraceRoot = TraceRoot;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtPmcRegisterTrace, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcRegisterTrace, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtPmcRegisterTrace_fn(NodeId, NumberOfCounters, Counters, TraceRoot);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcRegisterTrace, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtPmcUnregisterTrace_callback(HSAuint32   NodeId, HSATraceId  TraceId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtPmcUnregisterTrace.NodeId = NodeId;
  api_data.args.hsaKmtPmcUnregisterTrace.TraceId = TraceId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtPmcUnregisterTrace, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcUnregisterTrace, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtPmcUnregisterTrace_fn(NodeId, TraceId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcUnregisterTrace, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtPmcAcquireTraceAccess_callback(HSAuint32   NodeId, HSATraceId  TraceId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtPmcAcquireTraceAccess.NodeId = NodeId;
  api_data.args.hsaKmtPmcAcquireTraceAccess.TraceId = TraceId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtPmcAcquireTraceAccess, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcAcquireTraceAccess, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtPmcAcquireTraceAccess_fn(NodeId, TraceId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcAcquireTraceAccess, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtPmcReleaseTraceAccess_callback(HSAuint32   NodeId, HSATraceId  TraceId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtPmcReleaseTraceAccess.NodeId = NodeId;
  api_data.args.hsaKmtPmcReleaseTraceAccess.TraceId = TraceId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtPmcReleaseTraceAccess, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcReleaseTraceAccess, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtPmcReleaseTraceAccess_fn(NodeId, TraceId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcReleaseTraceAccess, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtPmcStartTrace_callback(HSATraceId  TraceId, void* TraceBuffer, HSAuint64   TraceBufferSizeBytes) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtPmcStartTrace.TraceId = TraceId;
  api_data.args.hsaKmtPmcStartTrace.TraceBuffer = TraceBuffer;
  api_data.args.hsaKmtPmcStartTrace.TraceBufferSizeBytes = TraceBufferSizeBytes;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtPmcStartTrace, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcStartTrace, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtPmcStartTrace_fn(TraceId, TraceBuffer, TraceBufferSizeBytes);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcStartTrace, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtPmcQueryTrace_callback(HSATraceId    TraceId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtPmcQueryTrace.TraceId = TraceId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtPmcQueryTrace, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcQueryTrace, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtPmcQueryTrace_fn(TraceId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcQueryTrace, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtPmcStopTrace_callback(HSATraceId  TraceId) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtPmcStopTrace.TraceId = TraceId;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtPmcStopTrace, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcStopTrace, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtPmcStopTrace_fn(TraceId);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtPmcStopTrace, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSetTrapHandler_callback(HSAuint32           NodeId, void* TrapHandlerBaseAddress, HSAuint64           TrapHandlerSizeInBytes, void* TrapBufferBaseAddress, HSAuint64           TrapBufferSizeInBytes) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSetTrapHandler.NodeId = NodeId;
  api_data.args.hsaKmtSetTrapHandler.TrapHandlerBaseAddress = TrapHandlerBaseAddress;
  api_data.args.hsaKmtSetTrapHandler.TrapHandlerSizeInBytes = TrapHandlerSizeInBytes;
  api_data.args.hsaKmtSetTrapHandler.TrapBufferBaseAddress = TrapBufferBaseAddress;
  api_data.args.hsaKmtSetTrapHandler.TrapBufferSizeInBytes = TrapBufferSizeInBytes;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSetTrapHandler, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetTrapHandler, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSetTrapHandler_fn(NodeId, TrapHandlerBaseAddress, TrapHandlerSizeInBytes, TrapBufferBaseAddress, TrapBufferSizeInBytes);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetTrapHandler, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetTileConfig_callback(HSAuint32           NodeId, HsaGpuTileConfig* config) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetTileConfig.NodeId = NodeId;
  api_data.args.hsaKmtGetTileConfig.config = config;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetTileConfig, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetTileConfig, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetTileConfig_fn(NodeId, config);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetTileConfig, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtQueryPointerInfo_callback(const void* Pointer, HsaPointerInfo* PointerInfo) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtQueryPointerInfo.Pointer = Pointer;
  api_data.args.hsaKmtQueryPointerInfo.PointerInfo = PointerInfo;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtQueryPointerInfo, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtQueryPointerInfo, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtQueryPointerInfo_fn(Pointer, PointerInfo);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtQueryPointerInfo, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSetMemoryUserData_callback(const void* Pointer, void* UserData) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSetMemoryUserData.Pointer = Pointer;
  api_data.args.hsaKmtSetMemoryUserData.UserData = UserData;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSetMemoryUserData, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetMemoryUserData, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSetMemoryUserData_fn(Pointer, UserData);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetMemoryUserData, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSPMAcquire_callback(HSAuint32	PreferredNode) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSPMAcquire.PreferredNode = PreferredNode;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSPMAcquire, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSPMAcquire, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSPMAcquire_fn(PreferredNode);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSPMAcquire, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSPMRelease_callback(HSAuint32	PreferredNode) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSPMRelease.PreferredNode = PreferredNode;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSPMRelease, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSPMRelease, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSPMRelease_fn(PreferredNode);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSPMRelease, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSPMSetDestBuffer_callback(HSAuint32   PreferredNode, HSAuint32   SizeInBytes, HSAuint32* timeout, HSAuint32* SizeCopied, void* DestMemoryAddress, bool* isSPMDataLoss) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSPMSetDestBuffer.PreferredNode = PreferredNode;
  api_data.args.hsaKmtSPMSetDestBuffer.SizeInBytes = SizeInBytes;
  api_data.args.hsaKmtSPMSetDestBuffer.timeout = timeout;
  api_data.args.hsaKmtSPMSetDestBuffer.SizeCopied = SizeCopied;
  api_data.args.hsaKmtSPMSetDestBuffer.DestMemoryAddress = DestMemoryAddress;
  api_data.args.hsaKmtSPMSetDestBuffer.isSPMDataLoss = isSPMDataLoss;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSPMSetDestBuffer, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSPMSetDestBuffer, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSPMSetDestBuffer_fn(PreferredNode, SizeInBytes, timeout, SizeCopied, DestMemoryAddress, isSPMDataLoss);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSPMSetDestBuffer, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSVMSetAttr_callback(void* start_addr, HSAuint64 size, unsigned int nattr, HSA_SVM_ATTRIBUTE* attrs) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSVMSetAttr.start_addr = start_addr;
  api_data.args.hsaKmtSVMSetAttr.size = size;
  api_data.args.hsaKmtSVMSetAttr.nattr = nattr;
  api_data.args.hsaKmtSVMSetAttr.attrs = attrs;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSVMSetAttr, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSVMSetAttr, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSVMSetAttr_fn(start_addr, size, nattr, attrs);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSVMSetAttr, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSVMGetAttr_callback(void* start_addr, HSAuint64 size, unsigned int nattr, HSA_SVM_ATTRIBUTE* attrs) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSVMGetAttr.start_addr = start_addr;
  api_data.args.hsaKmtSVMGetAttr.size = size;
  api_data.args.hsaKmtSVMGetAttr.nattr = nattr;
  api_data.args.hsaKmtSVMGetAttr.attrs = attrs;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSVMGetAttr, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSVMGetAttr, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSVMGetAttr_fn(start_addr, size, nattr, attrs);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSVMGetAttr, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtSetXNACKMode_callback(HSAint32 enable) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtSetXNACKMode.enable = enable;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtSetXNACKMode, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetXNACKMode, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtSetXNACKMode_fn(enable);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtSetXNACKMode, &api_data, api_callback_arg);
  return ret;
}
HSAKMT_STATUS hsaKmtGetXNACKMode_callback(HSAint32* enable) {
  if (HSAKMTAPI_table == NULL) intercept_KFDApiTable();
  kfd_api_data_t api_data{};
  api_data.args.hsaKmtGetXNACKMode.enable = enable;
  activity_rtapi_callback_t api_callback_fun = NULL;
  void* api_callback_arg = NULL;
  cb_table.get(KFD_API_ID_hsaKmtGetXNACKMode, &api_callback_fun, &api_callback_arg);
  api_data.phase = 0;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetXNACKMode, &api_data, api_callback_arg);
  HSAKMT_STATUS ret =   HSAKMTAPI_table->hsaKmtGetXNACKMode_fn(enable);
  api_data.HSAKMT_STATUS_retval = ret;
  api_data.phase = 1;
  if (api_callback_fun) api_callback_fun(ACTIVITY_DOMAIN_KFD_API, KFD_API_ID_hsaKmtGetXNACKMode, &api_data, api_callback_arg);
  return ret;
}

};};
#endif // PROF_API_IMPL

// section: API output stream

#ifdef __cplusplus
typedef std::pair<uint32_t, kfd_api_data_t> kfd_api_data_pair_t;
inline std::ostream& operator<< (std::ostream& out, const kfd_api_data_pair_t& data_pair) {
  const uint32_t cid = data_pair.first;
  const kfd_api_data_t& api_data = data_pair.second;
  switch(cid) {
    // block: HSAKMTAPI API
    case KFD_API_ID_hsaKmtOpenKFD: {
      out << "hsaKmtOpenKFD(";
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtCloseKFD: {
      out << "hsaKmtCloseKFD(";
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetVersion: {
      out << "hsaKmtGetVersion(";
      out << api_data.args.hsaKmtGetVersion.VersionInfo;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtAcquireSystemProperties: {
      out << "hsaKmtAcquireSystemProperties(";
      out << api_data.args.hsaKmtAcquireSystemProperties.SystemProperties;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtReleaseSystemProperties: {
      out << "hsaKmtReleaseSystemProperties(";
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetNodeProperties: {
      out << "hsaKmtGetNodeProperties(";
      out << api_data.args.hsaKmtGetNodeProperties.NodeId << ", ";
      out << api_data.args.hsaKmtGetNodeProperties.NodeProperties;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetNodeMemoryProperties: {
      out << "hsaKmtGetNodeMemoryProperties(";
      out << api_data.args.hsaKmtGetNodeMemoryProperties.NodeId << ", ";
      out << api_data.args.hsaKmtGetNodeMemoryProperties.NumBanks << ", ";
      out << api_data.args.hsaKmtGetNodeMemoryProperties.MemoryProperties;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetNodeCacheProperties: {
      out << "hsaKmtGetNodeCacheProperties(";
      out << api_data.args.hsaKmtGetNodeCacheProperties.NodeId << ", ";
      out << api_data.args.hsaKmtGetNodeCacheProperties.ProcessorId << ", ";
      out << api_data.args.hsaKmtGetNodeCacheProperties.NumCaches << ", ";
      out << api_data.args.hsaKmtGetNodeCacheProperties.CacheProperties;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetNodeIoLinkProperties: {
      out << "hsaKmtGetNodeIoLinkProperties(";
      out << api_data.args.hsaKmtGetNodeIoLinkProperties.NodeId << ", ";
      out << api_data.args.hsaKmtGetNodeIoLinkProperties.NumIoLinks << ", ";
      out << api_data.args.hsaKmtGetNodeIoLinkProperties.IoLinkProperties;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtCreateEvent: {
      out << "hsaKmtCreateEvent(";
      out << api_data.args.hsaKmtCreateEvent.EventDesc << ", ";
      out << api_data.args.hsaKmtCreateEvent.ManualReset << ", ";
      out << api_data.args.hsaKmtCreateEvent.IsSignaled << ", ";
      out << api_data.args.hsaKmtCreateEvent.Event;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtDestroyEvent: {
      out << "hsaKmtDestroyEvent(";
      out << api_data.args.hsaKmtDestroyEvent.Event;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSetEvent: {
      out << "hsaKmtSetEvent(";
      out << api_data.args.hsaKmtSetEvent.Event;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtResetEvent: {
      out << "hsaKmtResetEvent(";
      out << api_data.args.hsaKmtResetEvent.Event;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtQueryEventState: {
      out << "hsaKmtQueryEventState(";
      out << api_data.args.hsaKmtQueryEventState.Event;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtWaitOnEvent: {
      out << "hsaKmtWaitOnEvent(";
      out << api_data.args.hsaKmtWaitOnEvent.Event << ", ";
      out << api_data.args.hsaKmtWaitOnEvent.Milliseconds;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtWaitOnMultipleEvents: {
      out << "hsaKmtWaitOnMultipleEvents(";
      out << api_data.args.hsaKmtWaitOnMultipleEvents.Events << ", ";
      out << api_data.args.hsaKmtWaitOnMultipleEvents.NumEvents << ", ";
      out << api_data.args.hsaKmtWaitOnMultipleEvents.WaitOnAll << ", ";
      out << api_data.args.hsaKmtWaitOnMultipleEvents.Milliseconds;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtReportQueue: {
      out << "hsaKmtReportQueue(";
      out << api_data.args.hsaKmtReportQueue.QueueId << ", ";
      out << api_data.args.hsaKmtReportQueue.QueueReport;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtCreateQueue: {
      out << "hsaKmtCreateQueue(";
      out << api_data.args.hsaKmtCreateQueue.NodeId << ", ";
      out << api_data.args.hsaKmtCreateQueue.Type << ", ";
      out << api_data.args.hsaKmtCreateQueue.QueuePercentage << ", ";
      out << api_data.args.hsaKmtCreateQueue.Priority << ", ";
      out << api_data.args.hsaKmtCreateQueue.QueueAddress << ", ";
      out << api_data.args.hsaKmtCreateQueue.QueueSizeInBytes << ", ";
      out << api_data.args.hsaKmtCreateQueue.Event << ", ";
      out << api_data.args.hsaKmtCreateQueue.QueueResource;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtUpdateQueue: {
      out << "hsaKmtUpdateQueue(";
      out << api_data.args.hsaKmtUpdateQueue.QueueId << ", ";
      out << api_data.args.hsaKmtUpdateQueue.QueuePercentage << ", ";
      out << api_data.args.hsaKmtUpdateQueue.Priority << ", ";
      out << api_data.args.hsaKmtUpdateQueue.QueueAddress << ", ";
      out << api_data.args.hsaKmtUpdateQueue.QueueSize << ", ";
      out << api_data.args.hsaKmtUpdateQueue.Event;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtDestroyQueue: {
      out << "hsaKmtDestroyQueue(";
      out << api_data.args.hsaKmtDestroyQueue.QueueId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSetQueueCUMask: {
      out << "hsaKmtSetQueueCUMask(";
      out << api_data.args.hsaKmtSetQueueCUMask.QueueId << ", ";
      out << api_data.args.hsaKmtSetQueueCUMask.CUMaskCount << ", ";
      out << api_data.args.hsaKmtSetQueueCUMask.QueueCUMask;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetQueueInfo: {
      out << "hsaKmtGetQueueInfo(";
      out << api_data.args.hsaKmtGetQueueInfo.QueueId << ", ";
      out << api_data.args.hsaKmtGetQueueInfo.QueueInfo;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSetMemoryPolicy: {
      out << "hsaKmtSetMemoryPolicy(";
      out << api_data.args.hsaKmtSetMemoryPolicy.Node << ", ";
      out << api_data.args.hsaKmtSetMemoryPolicy.DefaultPolicy << ", ";
      out << api_data.args.hsaKmtSetMemoryPolicy.AlternatePolicy << ", ";
      out << api_data.args.hsaKmtSetMemoryPolicy.MemoryAddressAlternate << ", ";
      out << api_data.args.hsaKmtSetMemoryPolicy.MemorySizeInBytes;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtAllocMemory: {
      out << "hsaKmtAllocMemory(";
      out << api_data.args.hsaKmtAllocMemory.PreferredNode << ", ";
      out << api_data.args.hsaKmtAllocMemory.SizeInBytes << ", ";
      out << api_data.args.hsaKmtAllocMemory.MemoryAddress;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtFreeMemory: {
      out << "hsaKmtFreeMemory(";
      out << api_data.args.hsaKmtFreeMemory.MemoryAddress << ", ";
      out << api_data.args.hsaKmtFreeMemory.SizeInBytes;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtRegisterMemory: {
      out << "hsaKmtRegisterMemory(";
      out << api_data.args.hsaKmtRegisterMemory.MemoryAddress << ", ";
      out << api_data.args.hsaKmtRegisterMemory.MemorySizeInBytes;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtRegisterMemoryToNodes: {
      out << "hsaKmtRegisterMemoryToNodes(";
      out << api_data.args.hsaKmtRegisterMemoryToNodes.MemoryAddress << ", ";
      out << api_data.args.hsaKmtRegisterMemoryToNodes.MemorySizeInBytes << ", ";
      out << api_data.args.hsaKmtRegisterMemoryToNodes.NumberOfNodes << ", ";
      out << api_data.args.hsaKmtRegisterMemoryToNodes.NodeArray;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtRegisterMemoryWithFlags: {
      out << "hsaKmtRegisterMemoryWithFlags(";
      out << api_data.args.hsaKmtRegisterMemoryWithFlags.MemoryAddress << ", ";
      out << api_data.args.hsaKmtRegisterMemoryWithFlags.MemorySizeInBytes << ", ";
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtRegisterGraphicsHandleToNodes: {
      out << "hsaKmtRegisterGraphicsHandleToNodes(";
      out << api_data.args.hsaKmtRegisterGraphicsHandleToNodes.GraphicsResourceHandle << ", ";
      out << api_data.args.hsaKmtRegisterGraphicsHandleToNodes.GraphicsResourceInfo << ", ";
      out << api_data.args.hsaKmtRegisterGraphicsHandleToNodes.NumberOfNodes << ", ";
      out << api_data.args.hsaKmtRegisterGraphicsHandleToNodes.NodeArray;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtShareMemory: {
      out << "hsaKmtShareMemory(";
      out << api_data.args.hsaKmtShareMemory.MemoryAddress << ", ";
      out << api_data.args.hsaKmtShareMemory.SizeInBytes << ", ";
      out << api_data.args.hsaKmtShareMemory.SharedMemoryHandle;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtRegisterSharedHandle: {
      out << "hsaKmtRegisterSharedHandle(";
      out << api_data.args.hsaKmtRegisterSharedHandle.SharedMemoryHandle << ", ";
      out << api_data.args.hsaKmtRegisterSharedHandle.MemoryAddress << ", ";
      out << api_data.args.hsaKmtRegisterSharedHandle.SizeInBytes;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtRegisterSharedHandleToNodes: {
      out << "hsaKmtRegisterSharedHandleToNodes(";
      out << api_data.args.hsaKmtRegisterSharedHandleToNodes.SharedMemoryHandle << ", ";
      out << api_data.args.hsaKmtRegisterSharedHandleToNodes.MemoryAddress << ", ";
      out << api_data.args.hsaKmtRegisterSharedHandleToNodes.SizeInBytes << ", ";
      out << api_data.args.hsaKmtRegisterSharedHandleToNodes.NumberOfNodes << ", ";
      out << api_data.args.hsaKmtRegisterSharedHandleToNodes.NodeArray;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtProcessVMRead: {
      out << "hsaKmtProcessVMRead(";
      out << api_data.args.hsaKmtProcessVMRead.Pid << ", ";
      out << api_data.args.hsaKmtProcessVMRead.LocalMemoryArray << ", ";
      out << api_data.args.hsaKmtProcessVMRead.LocalMemoryArrayCount << ", ";
      out << api_data.args.hsaKmtProcessVMRead.RemoteMemoryArray << ", ";
      out << api_data.args.hsaKmtProcessVMRead.RemoteMemoryArrayCount << ", ";
      out << api_data.args.hsaKmtProcessVMRead.SizeCopied;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtProcessVMWrite: {
      out << "hsaKmtProcessVMWrite(";
      out << api_data.args.hsaKmtProcessVMWrite.Pid << ", ";
      out << api_data.args.hsaKmtProcessVMWrite.LocalMemoryArray << ", ";
      out << api_data.args.hsaKmtProcessVMWrite.LocalMemoryArrayCount << ", ";
      out << api_data.args.hsaKmtProcessVMWrite.RemoteMemoryArray << ", ";
      out << api_data.args.hsaKmtProcessVMWrite.RemoteMemoryArrayCount << ", ";
      out << api_data.args.hsaKmtProcessVMWrite.SizeCopied;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtDeregisterMemory: {
      out << "hsaKmtDeregisterMemory(";
      out << api_data.args.hsaKmtDeregisterMemory.MemoryAddress;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtMapMemoryToGPU: {
      out << "hsaKmtMapMemoryToGPU(";
      out << api_data.args.hsaKmtMapMemoryToGPU.MemoryAddress << ", ";
      out << api_data.args.hsaKmtMapMemoryToGPU.MemorySizeInBytes << ", ";
      out << api_data.args.hsaKmtMapMemoryToGPU.AlternateVAGPU;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtMapMemoryToGPUNodes: {
      out << "hsaKmtMapMemoryToGPUNodes(";
      out << api_data.args.hsaKmtMapMemoryToGPUNodes.MemoryAddress << ", ";
      out << api_data.args.hsaKmtMapMemoryToGPUNodes.MemorySizeInBytes << ", ";
      out << api_data.args.hsaKmtMapMemoryToGPUNodes.AlternateVAGPU << ", ";
      out << api_data.args.hsaKmtMapMemoryToGPUNodes.MemMapFlags << ", ";
      out << api_data.args.hsaKmtMapMemoryToGPUNodes.NumberOfNodes << ", ";
      out << api_data.args.hsaKmtMapMemoryToGPUNodes.NodeArray;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtUnmapMemoryToGPU: {
      out << "hsaKmtUnmapMemoryToGPU(";
      out << api_data.args.hsaKmtUnmapMemoryToGPU.MemoryAddress;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtMapGraphicHandle: {
      out << "hsaKmtMapGraphicHandle(";
      out << api_data.args.hsaKmtMapGraphicHandle.NodeId << ", ";
      out << api_data.args.hsaKmtMapGraphicHandle.GraphicDeviceHandle << ", ";
      out << api_data.args.hsaKmtMapGraphicHandle.GraphicResourceHandle << ", ";
      out << api_data.args.hsaKmtMapGraphicHandle.GraphicResourceOffset << ", ";
      out << api_data.args.hsaKmtMapGraphicHandle.GraphicResourceSize << ", ";
      out << api_data.args.hsaKmtMapGraphicHandle.FlatMemoryAddress;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtUnmapGraphicHandle: {
      out << "hsaKmtUnmapGraphicHandle(";
      out << api_data.args.hsaKmtUnmapGraphicHandle.NodeId << ", ";
      out << api_data.args.hsaKmtUnmapGraphicHandle.FlatMemoryAddress << ", ";
      out << api_data.args.hsaKmtUnmapGraphicHandle.SizeInBytes;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtAllocQueueGWS: {
      out << "hsaKmtAllocQueueGWS(";
      out << api_data.args.hsaKmtAllocQueueGWS.QueueId << ", ";
      out << api_data.args.hsaKmtAllocQueueGWS.nGWS << ", ";
      out << api_data.args.hsaKmtAllocQueueGWS.firstGWS;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtDbgRegister: {
      out << "hsaKmtDbgRegister(";
      out << api_data.args.hsaKmtDbgRegister.NodeId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtDbgUnregister: {
      out << "hsaKmtDbgUnregister(";
      out << api_data.args.hsaKmtDbgUnregister.NodeId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtDbgWavefrontControl: {
      out << "hsaKmtDbgWavefrontControl(";
      out << api_data.args.hsaKmtDbgWavefrontControl.NodeId << ", ";
      out << api_data.args.hsaKmtDbgWavefrontControl.Operand << ", ";
      out << api_data.args.hsaKmtDbgWavefrontControl.Mode << ", ";
      out << api_data.args.hsaKmtDbgWavefrontControl.TrapId << ", ";
      out << api_data.args.hsaKmtDbgWavefrontControl.DbgWaveMsgRing;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtDbgAddressWatch: {
      out << "hsaKmtDbgAddressWatch(";
      out << api_data.args.hsaKmtDbgAddressWatch.NodeId << ", ";
      out << api_data.args.hsaKmtDbgAddressWatch.NumWatchPoints << ", ";
      out << api_data.args.hsaKmtDbgAddressWatch.WatchMode << ", ";
      out << api_data.args.hsaKmtDbgAddressWatch.WatchAddress << ", ";
      out << api_data.args.hsaKmtDbgAddressWatch.WatchMask << ", ";
      out << api_data.args.hsaKmtDbgAddressWatch.WatchEvent;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtQueueSuspend: {
      out << "hsaKmtQueueSuspend(";
      out << api_data.args.hsaKmtQueueSuspend.Pid << ", ";
      out << api_data.args.hsaKmtQueueSuspend.NumQueues << ", ";
      out << api_data.args.hsaKmtQueueSuspend.Queues << ", ";
      out << api_data.args.hsaKmtQueueSuspend.GracePeriod << ", ";
      out << api_data.args.hsaKmtQueueSuspend.Flags;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtQueueResume: {
      out << "hsaKmtQueueResume(";
      out << api_data.args.hsaKmtQueueResume.Pid << ", ";
      out << api_data.args.hsaKmtQueueResume.NumQueues << ", ";
      out << api_data.args.hsaKmtQueueResume.Queues << ", ";
      out << api_data.args.hsaKmtQueueResume.Flags;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtEnableDebugTrap: {
      out << "hsaKmtEnableDebugTrap(";
      out << api_data.args.hsaKmtEnableDebugTrap.NodeId << ", ";
      out << api_data.args.hsaKmtEnableDebugTrap.QueueId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtEnableDebugTrapWithPollFd: {
      out << "hsaKmtEnableDebugTrapWithPollFd(";
      out << api_data.args.hsaKmtEnableDebugTrapWithPollFd.NodeId << ", ";
      out << api_data.args.hsaKmtEnableDebugTrapWithPollFd.QueueId << ", ";
      out << api_data.args.hsaKmtEnableDebugTrapWithPollFd.PollFd;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtDisableDebugTrap: {
      out << "hsaKmtDisableDebugTrap(";
      out << api_data.args.hsaKmtDisableDebugTrap.NodeId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtQueryDebugEvent: {
      out << "hsaKmtQueryDebugEvent(";
      out << api_data.args.hsaKmtQueryDebugEvent.NodeId << ", ";
      out << api_data.args.hsaKmtQueryDebugEvent.Pid << ", ";
      out << api_data.args.hsaKmtQueryDebugEvent.QueueId << ", ";
      out << api_data.args.hsaKmtQueryDebugEvent.ClearEvents << ", ";
      out << api_data.args.hsaKmtQueryDebugEvent.EventsReceived << ", ";
      out << api_data.args.hsaKmtQueryDebugEvent.IsSuspended << ", ";
      out << api_data.args.hsaKmtQueryDebugEvent.IsNew;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetQueueSnapshot: {
      out << "hsaKmtGetQueueSnapshot(";
      out << api_data.args.hsaKmtGetQueueSnapshot.NodeId << ", ";
      out << api_data.args.hsaKmtGetQueueSnapshot.Pid << ", ";
      out << api_data.args.hsaKmtGetQueueSnapshot.ClearEvents << ", ";
      out << api_data.args.hsaKmtGetQueueSnapshot.SnapshotBuf << ", ";
      out << api_data.args.hsaKmtGetQueueSnapshot.QssEntries;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSendHostTrap: {
      out << "hsaKmtSendHostTrap(";
      out << api_data.args.hsaKmtSendHostTrap.NodeId << ", ";
      out << api_data.args.hsaKmtSendHostTrap.Pid;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSetWaveLaunchTrapOverride: {
      out << "hsaKmtSetWaveLaunchTrapOverride(";
      out << api_data.args.hsaKmtSetWaveLaunchTrapOverride.NodeId << ", ";
      out << api_data.args.hsaKmtSetWaveLaunchTrapOverride.TrapOverride << ", ";
      out << api_data.args.hsaKmtSetWaveLaunchTrapOverride.TrapMask;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSetWaveLaunchMode: {
      out << "hsaKmtSetWaveLaunchMode(";
      out << api_data.args.hsaKmtSetWaveLaunchMode.NodeId << ", ";
      out << api_data.args.hsaKmtSetWaveLaunchMode.WaveLaunchMode;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetKernelDebugTrapVersionInfo: {
      out << "hsaKmtGetKernelDebugTrapVersionInfo(";
      out << api_data.args.hsaKmtGetKernelDebugTrapVersionInfo.Major << ", ";
      out << api_data.args.hsaKmtGetKernelDebugTrapVersionInfo.Minor;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetThunkDebugTrapVersionInfo: {
      out << "hsaKmtGetThunkDebugTrapVersionInfo(";
      out << api_data.args.hsaKmtGetThunkDebugTrapVersionInfo.Major << ", ";
      out << api_data.args.hsaKmtGetThunkDebugTrapVersionInfo.Minor;
      out << ") = void";
      break;
    }
    case KFD_API_ID_hsaKmtSetAddressWatch: {
      out << "hsaKmtSetAddressWatch(";
      out << api_data.args.hsaKmtSetAddressWatch.NodeId << ", ";
      out << api_data.args.hsaKmtSetAddressWatch.Pid << ", ";
      out << api_data.args.hsaKmtSetAddressWatch.WatchMode << ", ";
      out << api_data.args.hsaKmtSetAddressWatch.WatchAddress << ", ";
      out << api_data.args.hsaKmtSetAddressWatch.WatchAddrMask << ", ";
      out << api_data.args.hsaKmtSetAddressWatch.WatchId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtClearAddressWatch: {
      out << "hsaKmtClearAddressWatch(";
      out << api_data.args.hsaKmtClearAddressWatch.NodeId << ", ";
      out << api_data.args.hsaKmtClearAddressWatch.Pid << ", ";
      out << api_data.args.hsaKmtClearAddressWatch.WatchId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtEnablePreciseMemoryOperations: {
      out << "hsaKmtEnablePreciseMemoryOperations(";
      out << api_data.args.hsaKmtEnablePreciseMemoryOperations.NodeId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtDisablePreciseMemoryOperations: {
      out << "hsaKmtDisablePreciseMemoryOperations(";
      out << api_data.args.hsaKmtDisablePreciseMemoryOperations.NodeId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetClockCounters: {
      out << "hsaKmtGetClockCounters(";
      out << api_data.args.hsaKmtGetClockCounters.NodeId << ", ";
      out << api_data.args.hsaKmtGetClockCounters.Counters;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtPmcGetCounterProperties: {
      out << "hsaKmtPmcGetCounterProperties(";
      out << api_data.args.hsaKmtPmcGetCounterProperties.NodeId << ", ";
      out << api_data.args.hsaKmtPmcGetCounterProperties.CounterProperties;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtPmcRegisterTrace: {
      out << "hsaKmtPmcRegisterTrace(";
      out << api_data.args.hsaKmtPmcRegisterTrace.NodeId << ", ";
      out << api_data.args.hsaKmtPmcRegisterTrace.NumberOfCounters << ", ";
      out << api_data.args.hsaKmtPmcRegisterTrace.Counters << ", ";
      out << api_data.args.hsaKmtPmcRegisterTrace.TraceRoot;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtPmcUnregisterTrace: {
      out << "hsaKmtPmcUnregisterTrace(";
      out << api_data.args.hsaKmtPmcUnregisterTrace.NodeId << ", ";
      out << api_data.args.hsaKmtPmcUnregisterTrace.TraceId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtPmcAcquireTraceAccess: {
      out << "hsaKmtPmcAcquireTraceAccess(";
      out << api_data.args.hsaKmtPmcAcquireTraceAccess.NodeId << ", ";
      out << api_data.args.hsaKmtPmcAcquireTraceAccess.TraceId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtPmcReleaseTraceAccess: {
      out << "hsaKmtPmcReleaseTraceAccess(";
      out << api_data.args.hsaKmtPmcReleaseTraceAccess.NodeId << ", ";
      out << api_data.args.hsaKmtPmcReleaseTraceAccess.TraceId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtPmcStartTrace: {
      out << "hsaKmtPmcStartTrace(";
      out << api_data.args.hsaKmtPmcStartTrace.TraceId << ", ";
      out << api_data.args.hsaKmtPmcStartTrace.TraceBuffer << ", ";
      out << api_data.args.hsaKmtPmcStartTrace.TraceBufferSizeBytes;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtPmcQueryTrace: {
      out << "hsaKmtPmcQueryTrace(";
      out << api_data.args.hsaKmtPmcQueryTrace.TraceId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtPmcStopTrace: {
      out << "hsaKmtPmcStopTrace(";
      out << api_data.args.hsaKmtPmcStopTrace.TraceId;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSetTrapHandler: {
      out << "hsaKmtSetTrapHandler(";
      out << api_data.args.hsaKmtSetTrapHandler.NodeId << ", ";
      out << api_data.args.hsaKmtSetTrapHandler.TrapHandlerBaseAddress << ", ";
      out << api_data.args.hsaKmtSetTrapHandler.TrapHandlerSizeInBytes << ", ";
      out << api_data.args.hsaKmtSetTrapHandler.TrapBufferBaseAddress << ", ";
      out << api_data.args.hsaKmtSetTrapHandler.TrapBufferSizeInBytes;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetTileConfig: {
      out << "hsaKmtGetTileConfig(";
      out << api_data.args.hsaKmtGetTileConfig.NodeId << ", ";
      out << api_data.args.hsaKmtGetTileConfig.config;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtQueryPointerInfo: {
      out << "hsaKmtQueryPointerInfo(";
      out << api_data.args.hsaKmtQueryPointerInfo.Pointer << ", ";
      out << api_data.args.hsaKmtQueryPointerInfo.PointerInfo;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSetMemoryUserData: {
      out << "hsaKmtSetMemoryUserData(";
      out << api_data.args.hsaKmtSetMemoryUserData.Pointer << ", ";
      out << api_data.args.hsaKmtSetMemoryUserData.UserData;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSPMAcquire: {
      out << "hsaKmtSPMAcquire(";
      out << api_data.args.hsaKmtSPMAcquire.PreferredNode;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSPMRelease: {
      out << "hsaKmtSPMRelease(";
      out << api_data.args.hsaKmtSPMRelease.PreferredNode;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSPMSetDestBuffer: {
      out << "hsaKmtSPMSetDestBuffer(";
      out << api_data.args.hsaKmtSPMSetDestBuffer.PreferredNode << ", ";
      out << api_data.args.hsaKmtSPMSetDestBuffer.SizeInBytes << ", ";
      out << api_data.args.hsaKmtSPMSetDestBuffer.timeout << ", ";
      out << api_data.args.hsaKmtSPMSetDestBuffer.SizeCopied << ", ";
      out << api_data.args.hsaKmtSPMSetDestBuffer.DestMemoryAddress << ", ";
      out << api_data.args.hsaKmtSPMSetDestBuffer.isSPMDataLoss;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSVMSetAttr: {
      out << "hsaKmtSVMSetAttr(";
      out << api_data.args.hsaKmtSVMSetAttr.start_addr << ", ";
      out << api_data.args.hsaKmtSVMSetAttr.size << ", ";
      out << api_data.args.hsaKmtSVMSetAttr.nattr << ", ";
      out << api_data.args.hsaKmtSVMSetAttr.attrs;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSVMGetAttr: {
      out << "hsaKmtSVMGetAttr(";
      out << api_data.args.hsaKmtSVMGetAttr.start_addr << ", ";
      out << api_data.args.hsaKmtSVMGetAttr.size << ", ";
      out << api_data.args.hsaKmtSVMGetAttr.nattr << ", ";
      out << api_data.args.hsaKmtSVMGetAttr.attrs;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtSetXNACKMode: {
      out << "hsaKmtSetXNACKMode(";
      out << api_data.args.hsaKmtSetXNACKMode.enable;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    case KFD_API_ID_hsaKmtGetXNACKMode: {
      out << "hsaKmtGetXNACKMode(";
      out << api_data.args.hsaKmtGetXNACKMode.enable;
      out << ") = " << api_data.HSAKMT_STATUS_retval;
      break;
    }
    default:
      out << "ERROR: unknown API";
      abort();
  }
  return out;
}
#endif
#endif // INC_KFD_PROF_STR_H_