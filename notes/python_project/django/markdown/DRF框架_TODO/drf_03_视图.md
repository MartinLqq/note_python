

# DRF 视图



```
Request 与 Response
视图概览
	==== view.py ====
	APIView (DRF 视图基类, 继承自 Django 的 View)
	==== generics.py ====
	GenericAPIView (DRF 通用视图的基类, 继承自 APIView)
	CreateAPIView(CreateModelMixin, GenericAPIView)
	ListAPIView(ListModelMixin, GenericAPIView)
	RetrieveAPIView(RetrieveModelMixin, GenericAPIView)
	DestroyAPIView(DestroyModelMixin, GenericAPIView)
	UpdateAPIView(UpdateModelMixin, GenericAPIView)
	ListCreateAPIView(
		ListModelMixin, CreateModelMixin, GenericAPIView
	)
	RetrieveUpdateAPIView(
		RetrieveModelMixin, UpdateModelMixin, GenericAPIView
	)
	RetrieveDestroyAPIView(
		RetrieveModelMixin, DestroyModelMixin, GenericAPIView
	)
	RetrieveUpdateDestroyAPIView(
		RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView
	)
	
视图集 ViewSet
	==== viewsets.py ====
	ViewSet(ViewSetMixin, views.APIView)
	GenericViewSet(ViewSetMixin, GenericAPIView)
	ReadOnlyModelViewSet(
		RetrieveModelMixin, ListModelMixin, GenericViewSet
	)
	ModelViewSet(
		CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, 
		DestroyModelMixin, ListModelMixin, GenericViewSet
	)

路由 Router


mixin 扩展类
	==== mixins.py ====
	CreateModelMixin
	ListModelMixin
	RetrieveModelMixin
	UpdateModelMixin
	DestroyModelMixin
	==== viewsets.py ====
	ViewSetMixin
```

